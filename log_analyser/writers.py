import json
from pathlib import Path
from typing import Any

_registry = {}


def register_writer(file_format: str):
    def wrapper(func):
        _registry[file_format] = func
        return func

    return wrapper


@register_writer("json")
def json_reader(file_path: Path, content: Any):
    json.dump(content, file_path)


def get_file_writer(file_format: str):
    if not file_format in _registry:
        raise NotImplementedError(f"Unsupported file format {file_format}")
    return _registry.get(file_format)()
