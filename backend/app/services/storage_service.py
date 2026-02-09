from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List, Tuple

from app.models.trip_member import TripMember
from app.models.virtual_file import VirtualFile
from app.models.file_chunk import FileChunk
from app.models.user_cloud_account import UserCloudAccount
from app.services.google_drive_service import (
    get_drive_client,
    ensure_app_folder,
    upload_chunk_to_drive,
    download_chunk_from_drive,
)

# =========================
# Service-level Exceptions
# =========================

class InsufficientStorageError(Exception):
    pass


class FileNotFoundError(Exception):
    pass


# =========================
# Upload Planning + Metadata
# =========================

def create_virtual_file_with_chunks(
    *,
    db: Session,
    trip_id: str,
    uploader_user_id: str,
    path: str,
    file_size: int,
    checksum: str | None = None,
) -> VirtualFile:
    """
    Plans storage across trip members who:
    - are part of the trip
    - have linked Google Drive
    - have allocated free bytes
    """

    # 🔒 Only members who can actually store data
    members: List[TripMember] = (
        db.execute(
            select(TripMember)
            .join(
                UserCloudAccount,
                TripMember.user_id == UserCloudAccount.user_id,
            )
            .where(
                TripMember.trip_id == trip_id,
                UserCloudAccount.provider == "google_drive",
            )
            .with_for_update()
        )
        .scalars()
        .all()
    )

    if not members:
        raise InsufficientStorageError(
            "No trip members with Google Drive linked"
        )

    # Compute free space
    free_map: List[Tuple[TripMember, int]] = []
    for m in members:
        free = m.allocated_bytes - m.used_bytes
        if free > 0:
            free_map.append((m, free))

    if not free_map:
        raise InsufficientStorageError("No free storage available")

    free_map.sort(key=lambda x: x[1], reverse=True)

    # Placement plan
    plan: List[Tuple[TripMember, int]] = []

    # Best-fit: single owner
    for member, free in free_map:
        if free >= file_size:
            plan = [(member, file_size)]
            break

    # Striping fallback
    if not plan:
        total_free = sum(free for _, free in free_map)
        if total_free < file_size:
            raise InsufficientStorageError("Insufficient pooled storage")

        remaining = file_size
        for member, free in free_map:
            if remaining <= 0:
                break
            take = min(free, remaining)
            plan.append((member, take))
            remaining -= take

        if remaining != 0:
            raise InsufficientStorageError("Failed to allocate full file")

    # Create VirtualFile
    virtual_file = VirtualFile(
        trip_id=trip_id,
        path=path,
        size_bytes=file_size,
        checksum=checksum,
        uploaded_by=uploader_user_id,
        status="pending",
        uploaded_bytes=0,
    )
    db.add(virtual_file)
    db.flush()

    # Create chunks
    offset = 0
    for member, size in plan:
        db.add(
            FileChunk(
                virtual_file_id=virtual_file.id,
                owner_user_id=member.user_id,
                provider="PENDING",
                provider_file_id="PENDING",
                offset_bytes=offset,
                size_bytes=size,
            )
        )
        member.used_bytes += size
        offset += size

    db.commit()
    db.refresh(virtual_file)

    print("[UPLOAD PLAN CREATED]", virtual_file.id)
    return virtual_file


# =========================
# Delete Virtual File
# =========================

def delete_virtual_file(
    *,
    db: Session,
    virtual_file_id: str,
):
    virtual_file = db.get(VirtualFile, virtual_file_id)
    if not virtual_file:
        raise FileNotFoundError("Virtual file not found")

    chunks = (
        db.execute(
            select(FileChunk)
            .where(FileChunk.virtual_file_id == virtual_file_id)
            .with_for_update()
        )
        .scalars()
        .all()
    )

    # Roll back quota
    for chunk in chunks:
        member = (
            db.execute(
                select(TripMember)
                .where(
                    TripMember.trip_id == virtual_file.trip_id,
                    TripMember.user_id == chunk.owner_user_id,
                )
                .with_for_update()
            )
            .scalar_one()
        )

        member.used_bytes -= chunk.size_bytes
        if member.used_bytes < 0:
            member.used_bytes = 0

    db.delete(virtual_file)
    db.commit()

    print("[DELETE SUCCESS]", virtual_file_id)


# =========================
# Mock Download (pre-drive)
# =========================

def iter_virtual_file_bytes(
    *,
    db: Session,
    virtual_file_id: str,
):
    virtual_file = db.get(VirtualFile, virtual_file_id)
    if not virtual_file:
        raise FileNotFoundError("Virtual file not found")

    chunks = (
        db.execute(
            select(FileChunk)
            .where(FileChunk.virtual_file_id == virtual_file_id)
            .order_by(FileChunk.offset_bytes)
        )
        .scalars()
        .all()
    )

    if not chunks:
        raise FileNotFoundError("No chunks found")

    for chunk in chunks:
        yield b"\x00" * chunk.size_bytes


# =========================
# Upload Mock Chunks
# =========================

def upload_chunks_to_google_drive(
    *,
    db: Session,
    virtual_file_id: str,
):
    virtual_file = db.get(VirtualFile, virtual_file_id)
    if not virtual_file:
        raise FileNotFoundError("Virtual file not found")

    chunks = (
        db.execute(
            select(FileChunk)
            .where(FileChunk.virtual_file_id == virtual_file_id)
            .order_by(FileChunk.offset_bytes)
        )
        .scalars()
        .all()
    )

    for chunk in chunks:
        account = (
            db.query(UserCloudAccount)
            .filter(
                UserCloudAccount.user_id == chunk.owner_user_id,
                UserCloudAccount.provider == "google_drive",
            )
            .first()
        )

        if not account:
            raise Exception(f"User {chunk.owner_user_id} has no Google Drive linked")

        drive = get_drive_client(account)
        folder_id = ensure_app_folder(drive)

        data = b"\x01" * chunk.size_bytes

        provider_file_id = upload_chunk_to_drive(
            drive=drive,
            folder_id=folder_id,
            chunk_name=f"chunk_{virtual_file.id}_{chunk.offset_bytes}.bin",
            data=data,
        )

        chunk.provider = "google_drive"
        chunk.provider_file_id = provider_file_id

    db.commit()


# =========================
# REAL Upload (Background)
# =========================

def upload_real_file_to_google_drive(
    db: Session,
    virtual_file_id: str,
    file_stream,
):
    """
    Sync function — required for FastAPI BackgroundTasks
    """

    virtual_file = db.get(VirtualFile, virtual_file_id)
    if not virtual_file:
        return

    virtual_file.status = "uploading"
    virtual_file.uploaded_bytes = 0
    db.commit()

    uploaded = 0

    try:
        chunks = (
            db.execute(
                select(FileChunk)
                .where(FileChunk.virtual_file_id == virtual_file_id)
                .order_by(FileChunk.offset_bytes)
            )
            .scalars()
            .all()
        )

        for chunk in chunks:
            account = (
                db.query(UserCloudAccount)
                .filter(
                    UserCloudAccount.user_id == chunk.owner_user_id,
                    UserCloudAccount.provider == "google_drive",
                )
                .first()
            )

            if not account:
                raise Exception(
                    f"User {chunk.owner_user_id} has allocated storage but no Drive linked"
                )

            drive = get_drive_client(account)
            folder_id = ensure_app_folder(drive)

            data = file_stream.read(chunk.size_bytes)
            if not data:
                raise Exception("Unexpected EOF while reading file")

            provider_file_id = upload_chunk_to_drive(
                drive=drive,
                folder_id=folder_id,
                chunk_name=f"chunk_{virtual_file.id}_{chunk.offset_bytes}.bin",
                data=data,
            )

            chunk.provider = "google_drive"
            chunk.provider_file_id = provider_file_id

            uploaded += chunk.size_bytes
            virtual_file.uploaded_bytes = uploaded
            db.commit()

        virtual_file.status = "completed"
        db.commit()
        print("[UPLOAD COMPLETED]", virtual_file.id)

    except Exception as e:
        virtual_file.status = "failed"
        db.commit()
        print("[UPLOAD FAILED]", str(e))
        return


# =========================
# REAL Download
# =========================

def stream_virtual_file_from_drive(
    *,
    db: Session,
    virtual_file_id: str,
):
    virtual_file = db.get(VirtualFile, virtual_file_id)
    if not virtual_file:
        raise FileNotFoundError("Virtual file not found")

    chunks = (
        db.execute(
            select(FileChunk)
            .where(FileChunk.virtual_file_id == virtual_file_id)
            .order_by(FileChunk.offset_bytes)
        )
        .scalars()
        .all()
    )

    if not chunks:
        raise FileNotFoundError("No chunks found")

    for chunk in chunks:
        account = (
            db.query(UserCloudAccount)
            .filter(
                UserCloudAccount.user_id == chunk.owner_user_id,
                UserCloudAccount.provider == "google_drive",
            )
            .first()
        )

        if not account:
            raise Exception("Chunk owner has no Google Drive linked")

        drive = get_drive_client(account)

        for data in download_chunk_from_drive(
            drive,
            provider_file_id=chunk.provider_file_id,
        ):
            yield data
