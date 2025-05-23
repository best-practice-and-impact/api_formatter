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

    @property
    def approved(self) -> bool:
        return self.status == UploadStatus.APPROVED
