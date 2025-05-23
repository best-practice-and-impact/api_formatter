from typing import Any, Dict, Tuple, Type, List
from pydantic import BaseModel, Field, create_model
from datetime import datetime

class ModelGenerator:
    """
    Dynamically generate Pydantic models from a nested schema dict.
    """

    @staticmethod
    def generate_model(model_name: str, schema: Dict[str, Any], model_cache=None) -> Type[BaseModel]:
        if model_cache is None:
            model_cache = {}

        if model_name in model_cache:
            return model_cache[model_name]

        def resolve_field(field_def: Dict[str, Any]) -> Tuple[Any, Any]:
            ftype = field_def.get("type")
            required = field_def.get("required", False)

            if ftype == "dict":
                nested_name = field_def.get("model_name", "NestedModel")
                nested_schema = field_def
                nested_fields = {k: v for k, v in nested_schema.items() if k != "type" and k != "model_name"}
                nested_model = ModelGenerator.generate_model(nested_name, nested_fields, model_cache)
                py_type = nested_model

                default = None if not required else ...
                return py_type, Field(default=default)

            elif ftype == "list":
                item_def = field_def.get("items", {"type": "string"})
                item_type, _ = resolve_field(item_def)
                py_type = List[item_type]

                default = None if not required else ...
                return py_type, Field(default=default)

            elif ftype == "string":
                py_type = str
            elif ftype == "int":
                py_type = int
            elif ftype == "float":
                py_type = float
            elif ftype == "bool":
                py_type = bool
            elif ftype == "datetime":
                py_type = datetime
            elif ftype == "enum":
                py_type = field_def["enum"]
            elif ftype == "any":
                py_type = Any
            else:
                raise ValueError(f"Unsupported type: {ftype}")

            if "default" in field_def:
                default_value = field_def["default"]
            elif required:
                default_value = ...
            else:
                default_value = None

            return py_type, Field(default=default_value)

        fields = {}

        for field_name, field_def in schema.items():
            # Fix: if field_def is not a dict, convert it to dict with type string + default
            if not isinstance(field_def, dict):
                field_def = {"type": "string", "default": field_def}

            # If no "type" key but field_def is dict -> assume nested dict type
            if "type" not in field_def and isinstance(field_def, dict):
                field_def["type"] = "dict"
                field_def["model_name"] = model_name + "_" + field_name.capitalize()

            py_type, default = resolve_field(field_def)
            fields[field_name] = (py_type, default)

        model = create_model(model_name, **fields)
        model_cache[model_name] = model
        return model
