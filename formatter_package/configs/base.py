from abc import ABC
from pathlib import Path
from typing import Any, Dict
import json
import yaml
from pydantic import ValidationError

from validators.model_generator import ModelGenerator


class BaseConfig(ABC):
    def __init__(self, schema: Dict[str, Any], model_name: str):
        self._schema = schema
        self._metadata = {}
        self._model = ModelGenerator.generate_model(model_name, schema)
        self._errors = {}

    def import_from_dict(self, new_data: Dict[str, Any]):
        try:
            validated = self._model(**new_data)
            self._metadata = validated.model_dump()
        except ValidationError as e:
            raise ValueError(f"Metadata validation failed:\n{e}")

    def set(self, key: str, value: Any):
        if key not in self._schema:
            raise KeyError(f"Invalid field '{key}'. Valid fields: {list(self._schema.keys())}")
        try:
            updated = dict(self._metadata)
            updated[key] = value
            validated = self._model(**updated)
            self._metadata = validated.model_dump()
        except ValidationError as e:
            raise ValueError(f"Validation failed while setting '{key}':\n{e}")

    def get(self, key: str) -> Any:
        return self._metadata.get(key)

    def export_to_json(self, directory: str):
        directory = Path(directory)
        directory.mkdir(parents=True, exist_ok=True)
        title = self._metadata.get("title") or self._metadata.get("edition_title") or "config"
        path = directory / f"{title}_metadata.json"
        with path.open("w") as f:
            json.dump(self._metadata, f, indent=4, default=str)

    def load_from_file(self, file_path: str) -> Dict[str, Any]:
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"{file_path} not found")

        with path.open("r") as f:
            data = json.load(f) if file_path.endswith(".json") else yaml.safe_load(f)

        self.import_from_dict(data)
        return data

    @property
    def metadata(self) -> Dict[str, Any]:
        return self._metadata
