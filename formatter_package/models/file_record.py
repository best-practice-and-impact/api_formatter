from enum import Enum

from models.user import User


class UploadStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"


class FileRecord:

    def __init__(self, uploader: User, path: str):
        self.id = None
        self.uploader = uploader
        self.path = path
        self.metadata = None
        self.status = UploadStatus.PENDING
        self.approved_by = None
        self.created_at = None

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "uploader": self.uploader.to_dict() if isinstance(self.uploader, User) else self.uploader,
            "path": self.path,
            "metadata": self.metadata,
            "status": self.status.value,
            "approved_by": self.approved_by.to_dict() if self.approved_by else None,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

    @property
    def approved(self) -> bool:
        return self.status == UploadStatus.APPROVED
