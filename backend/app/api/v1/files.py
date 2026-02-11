from fastapi import APIRouter, Depends, Query, HTTPException, UploadFile, File, BackgroundTasks
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from sqlalchemy import select


from app.core.database import get_db
from app.core.auth import get_current_user
from app.models.user import User
from app.models.virtual_file import VirtualFile

from app.services.storage_service import (
    create_virtual_file_with_chunks,
    delete_virtual_file,
    upload_real_file_to_google_drive,
    stream_virtual_file_from_drive,
    InsufficientStorageError,
    FileNotFoundError,
)

router = APIRouter(prefix="/files", tags=["files"])


# =========================
# Upload + Store (REAL, background)
# =========================

@router.post("/upload-and-store")
def upload_and_store_file(
    background_tasks: BackgroundTasks,
    trip_id: str = Query(...),
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    file_size = 0
    chunk_size = 1024 * 1024 

    while True:
        chunk = file.file.read(chunk_size)
        if not chunk:
            break
        file_size += len(chunk)

    file.file.seek(0)

    virtual_file = create_virtual_file_with_chunks(
        db=db,
        trip_id=trip_id,
        uploader_user_id=current_user.id,
        path=file.filename,
        file_size=file_size,
        checksum=None,
    )

    background_tasks.add_task(
        upload_real_file_to_google_drive,
        db,
        virtual_file.id,
        file.file,
    )

    return {
        "message": "Upload started",
        "virtual_file_id": virtual_file.id,
        "status": "uploading",
    }


# =========================
# Download (REAL reconstruction)
# =========================

@router.get("/{virtual_file_id}/download")
def download_file(
    virtual_file_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    stream = stream_virtual_file_from_drive(
        db=db,
        virtual_file_id=virtual_file_id.strip(),
    )

    return StreamingResponse(
        stream,
        media_type="application/octet-stream",
        headers={
            "Content-Disposition": f'attachment; filename="{virtual_file_id}"'
        },
    )


# =========================
# Status
# =========================

@router.get("/{virtual_file_id}/status")
def get_file_status(
    virtual_file_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    vf = db.get(VirtualFile, virtual_file_id.strip())
    if not vf:
        raise HTTPException(status_code=404, detail="File not found")

    progress = (
        int((vf.uploaded_bytes / vf.size_bytes) * 100)
        if vf.size_bytes and vf.uploaded_bytes is not None
        else 0
    )

    return {
        "virtual_file_id": vf.id,
        "status": vf.status,
        "uploaded_bytes": vf.uploaded_bytes,
        "size_bytes": vf.size_bytes,
        "progress_percent": progress,
    }


# =========================
# Delete
# =========================

@router.delete("/{virtual_file_id}")
def delete_file(
    virtual_file_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        delete_virtual_file(
            db=db,
            virtual_file_id=virtual_file_id.strip(),
        )
        return {"message": "File deleted successfully"}

    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))



@router.get("")
def list_files(
    trip_id: str = Query(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    files = (
        db.execute(
            select(VirtualFile)
            .where(VirtualFile.trip_id == trip_id)
            .order_by(VirtualFile.created_at.desc())
        )
        .scalars()
        .all()
    )

    return [
        {
            "id": f.id,
            "path": f.path,
            "status": f.status,
            "uploaded_bytes": f.uploaded_bytes,
            "size_bytes": f.size_bytes,
            "progress_percent": (
                int((f.uploaded_bytes / f.size_bytes) * 100)
                if f.size_bytes > 0 else 0
            ),
        }
        for f in files
    ]