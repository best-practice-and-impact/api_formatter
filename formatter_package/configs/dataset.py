from typing import Dict, Any

from configs.base import BaseConfig
from validators.model_generator import ModelGenerator
from validators.type_generator import DatasetType
from pathlib import Path
import os

class DatasetConfig(BaseConfig):
    def __init__(self, schema: Dict[str, Any]):
        super().__init__(schema, "DatasetModel")

    def set(self, key: str, value: Any):
        if key == "type" and not isinstance(value, DatasetType):
            value = DatasetType(value)

        elif key == "file":
            value = self._process_file(value)

        super().set(key, value)

    def import_from_dict(self, new_data: Dict[str, Any]):
        if "file" in new_data and isinstance(new_data["file"], (str, Path)):
            new_data["file"] = self._process_file(new_data["file"])
        super().import_from_dict(new_data)

    def _process_file(self, file_path: str) -> dict:
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        return {
            "path": str(file_path),
            "format": file_path.suffix.lstrip('.'),
            "size": os.path.getsize(file_path)
        }
