from pydantic import BaseModel


class FileUploadRequest(BaseModel):
    path: str
    size_bytes: int
    checksum: str | None = None
