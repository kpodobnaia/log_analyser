from pathlib import Path
from typing import Any

from log_analyser.io.base import IOContext, Strategy


class OutputWriterStrategy(Strategy):
    def write(self, file_path: Path, content: Any) -> None:
        raise NotImplementedError


class OutputWriter(IOContext):
    _selected_strategy: OutputWriterStrategy
    NOT_IMPLEMENTED_MESSAGE = (
        "No output writer is implemented for {file_format} file format"
    )

    def write(self, file_path: Path, content: Any) -> None:
        self._selected_strategy.write(file_path, content)
