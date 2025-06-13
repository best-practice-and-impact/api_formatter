import base64
from datetime import datetime
from enum import Enum
from pathlib import Path


def custom_serialize(obj, seen=None):
    if seen is None:
        seen = set()

    obj_id = id(obj)
    if obj_id in seen:
        return f"<CircularRef: {type(obj)._name_}>"

    seen.add(obj_id)

    if isinstance(obj, Enum):
        return obj.value
    elif isinstance(obj, Path):
        return str(obj)
    elif isinstance(obj, datetime):
        return obj.isoformat()
    elif isinstance(obj, bytes):
        try:
            return obj.decode('utf-8')
        except UnicodeDecodeError:
            return base64.b64encode(obj).decode('utf-8')
    elif isinstance(obj, dict):
        return {k: custom_serialize(v, seen) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [custom_serialize(i, seen) for i in obj]
    elif hasattr(obj, "_metadata"):
        return custom_serialize(obj.metadata, seen)
    elif hasattr(obj, "_dict_"):
        return custom_serialize(vars(obj), seen)
    else:
        return str(obj)