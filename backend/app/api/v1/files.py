from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.file_upload import FileUploadRequest
from app.services.storage_service import (
    create_virtual_file_with_chunks,
    delete_virtual_file,
    InsufficientStorageError,
    FileNotFoundError,
)

from fastapi.responses import StreamingResponse
from app.services.storage_service import iter_virtual_file_bytes
from app.services.storage_service import upload_chunks_to_google_drive

router = APIRouter(prefix="/files", tags=["files"])


# =========================
# Upload API
# =========================

@router.post("")
def upload_file(
    payload: FileUploadRequest,
    trip_id: str = Query(..., description="Trip ID"),
    user_id: str = Query(..., description="Uploader User ID"),
    db: Session = Depends(get_db),
):
    try:
        virtual_file = create_virtual_file_with_chunks(
            db=db,
            trip_id=trip_id,
            uploader_user_id=user_id,
            path=payload.path,
            file_size=payload.size_bytes,
            checksum=payload.checksum,
        )
        return {
            "id": virtual_file.id,
            "path": virtual_file.path,
            "size_bytes": virtual_file.size_bytes,
        }

    except InsufficientStorageError as e:
        raise HTTPException(status_code=400, detail=str(e))


# =========================
# Delete API
# =========================

@router.delete("/{virtual_file_id}")
def delete_file(
    virtual_file_id: str,
    db: Session = Depends(get_db),
):
    virtual_file_id = virtual_file_id.strip()  # sanitize input

    try:
        delete_virtual_file(
            db=db,
            virtual_file_id=virtual_file_id,
        )
        return {"message": "File deleted successfully"}

    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

# =========================
# Download API
# =========================

@router.get("/{virtual_file_id}/download")
def download_file(
    virtual_file_id: str,
    db: Session = Depends(get_db),
):
    virtual_file_id = virtual_file_id.strip()

    try:
        byte_iterator = iter_virtual_file_bytes(
            db=db,
            virtual_file_id=virtual_file_id,
        )

        return StreamingResponse(
            byte_iterator,
            media_type="application/octet-stream",
        )

    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))



# =========================
# Google Drive Upload API
# =======================
@router.post("/{virtual_file_id}/upload_to_drive")
def upload_file_to_drive(
    virtual_file_id:str,
    db:Session =Depends(get_db),

):
    Virtual_file_id = virtual_file_id.strip()

    upload_chunks_to_google_drive(
        db=db,
        virtual_file_id=virtual_file_id,
    )

    return {"message":"File uploaded to Google Drive successfully"}