from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List, Tuple

from app.models.trip_member import TripMember
from app.models.virtual_file import VirtualFile
from app.models.file_chunk import FileChunk
from app.models.user_cloud_account import UserCloudAccount
from app.services.google_drive_service import get_drive_client, ensure_app_folder, upload_chunk_to_drive


# =========================
# Service-level Exceptions
# =========================

class InsufficientStorageError(Exception):
    pass


class FileNotFoundError(Exception):
    pass


# =========================
# Upload Service
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

    members: List[TripMember] = (
        db.execute(
            select(TripMember)
            .where(TripMember.trip_id == trip_id)
            .with_for_update()
        )
        .scalars()
        .all()
    )

    if not members:
        raise InsufficientStorageError("No members found for trip")

    free_map: List[Tuple[TripMember, int]] = []
    for m in members:
        free = m.allocated_bytes - m.used_bytes
        if free > 0:
            free_map.append((m, free))

    if not free_map:
        raise InsufficientStorageError("No free storage available")

    free_map.sort(key=lambda x: x[1], reverse=True)

    plan: List[Tuple[TripMember, int]] = []

    for member, free in free_map:
        if free >= file_size:
            plan = [(member, file_size)]
            break

    if not plan:
        total_free = sum(free for _, free in free_map)
        if total_free < file_size:
            raise InsufficientStorageError("Insufficient pooled storage")

        remaining = file_size
        for member, free in free_map:
            if remaining <= 0:
                break

            take = min(free, remaining)
            if take > 0:
                plan.append((member, take))
                remaining -= take

        if remaining != 0:
            raise InsufficientStorageError("Failed to allocate full file")

    virtual_file = VirtualFile(
        trip_id=trip_id,
        path=path,
        size_bytes=file_size,
        checksum=checksum,
        uploaded_by=uploader_user_id,
    )
    db.add(virtual_file)
    db.flush()

    offset = 0
    for member, size in plan:
        chunk = FileChunk(
            virtual_file_id=virtual_file.id,
            owner_user_id=member.user_id,
            provider="PENDING",
            provider_file_id="PENDING",
            offset_bytes=offset,
            size_bytes=size,
        )
        db.add(chunk)

        member.used_bytes += size
        offset += size

    db.commit()
    db.refresh(virtual_file)

    print("UPLOAD SUCCESS")
    print("VirtualFile ID:", virtual_file.id)
    print("DB URL:", db.bind.url)

    return virtual_file


# =========================
# Delete Service
# =========================

def delete_virtual_file(
    *,
    db: Session,
    virtual_file_id: str,
):
    print("DELETE REQUEST FOR FILE ID:", virtual_file_id)
    print("DB URL:", db.bind.url)

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

    print("DELETE SUCCESS:", virtual_file_id)


# chunk reconstruction(mocked btytes    )

def iter_virtual_file_bytes(
    *,
    db: Session,
    virtual_file_id: str,
):
    """
    Yields bytes of a virtual file in correct order.
    (Cloud fetch is mocked for now)
    """

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
        raise FileNotFoundError("No chunks found for file")

    for chunk in chunks:
        # MOCK: simulate chunk bytes
        yield b"\x00" * chunk.size_bytes


def upload_chunks_to_google_drive(
    *,
    db: Session,
    virtual_file_id: str,
):
    """
    Uploads all chunks of a VirtualFile to the respective
    owners' Google Drives and updates provider_file_id.
    """

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
        # 1. Get owner's Google account
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

        # 2. Drive client + app folder
        drive = get_drive_client(account)
        folder_id = ensure_app_folder(drive)

        # 3. Generate fake data (for now)
        data = b"\x01" * chunk.size_bytes

        chunk_name = f"chunk_{virtual_file.id}_{chunk.offset_bytes}.bin"

        # 4. Upload
        provider_file_id = upload_chunk_to_drive(
            drive,
            folder_id=folder_id,
            chunk_name=chunk_name,
            data=data,
        )

        # 5. Update DB
        chunk.provider = "google_drive"
        chunk.provider_file_id = provider_file_id

    db.commit()
