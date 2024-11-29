from pathlib import Path
from typing import Any

from log_analyser.io.base import IOContext, Strategy


class OutputWriterStrategy(Strategy):
    def write(self, file_path: Path, content: Any) -> None:
        raise NotImplementedError


class OutputWriter(IOContext):
    _selected_strategy: OutputWriterStrategy

    def write(self, file_path: Path, content: Any) -> None:
        self._selected_strategy.write(file_path, content)
