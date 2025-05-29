from models.file_record import FileRecord, UploadStatus
from models.user import Role
from configs.dataset import DatasetConfig
from configs.edition import EditionConfig
from services.db_service import DatabaseService
from validators.type_generator import VALIDATION_SCHEMA

class UploaderService:

    def __init__(self):
        self.dataset_schema = VALIDATION_SCHEMA["dataset"]
        self.edition_schema = VALIDATION_SCHEMA["edition"]

    def _check_permission(self, user):
        if user.role not in {Role.UPLOADER, Role.APPROVER}:
            raise PermissionError(f"User {user.username} does not have permission to perform this action.")

    def _upload(self, user, file_path: str, config_class, schema, is_edition=False) -> FileRecord:
        self._check_permission(user)
        config = config_class(schema)
        config.load_from_file(file_path)

        record = FileRecord(user, file_path)
        record.metadata = config.metadata
        record.status = UploadStatus.PENDING
        record.metadata['is_edition'] = "True" if is_edition else "False"
        return record

    def upload_dataset(self, user, file_path: str) -> FileRecord:
        return self._upload(user, file_path, DatasetConfig, self.dataset_schema)


    def upload_edition(self, user, file_path: str, is_edition=True) -> FileRecord:
        return self._upload(user, file_path, EditionConfig, self.edition_schema, is_edition)


    def preview(self, record: FileRecord):
        return record.metadata

    def edit_metadata(self, user, record: FileRecord, new_data: dict):
        self._check_permission(user)

        if record.metadata.get("is_edition") == "True":                    
            config = EditionConfig(self.edition_schema)
        else:
            config = DatasetConfig(self.dataset_schema)

        try:
            config.import_from_dict(new_data=new_data)
        except ValueError as e:
            raise ValueError(f"Metadata validation failed:\n{e}")

        record.metadata = config.metadata
        return record.metadata


    def save(self, db: DatabaseService, record: FileRecord):
        db.add_file_record(record)
        return record