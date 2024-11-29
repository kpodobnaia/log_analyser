_registry = {}


def register_reader(file_format: str):
    def wrapper(func):
        _registry[file_format] = func
        return func

    return wrapper


def get_file_reader(file_format: str):
    if not file_format in _registry:
        raise NotImplementedError(f"Unsupported file format {file_format}")
    return _registry.get(file_format)
