from configs.base import BaseConfig
from validators.model_generator import ModelGenerator
from typing import Dict, Any

class EditionConfig(BaseConfig):
    def __init__(self, schema: Dict[str, Any]):
        super().__init__(schema, "EditionModel")
