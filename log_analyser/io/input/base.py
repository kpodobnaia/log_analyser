from pathlib import Path
from typing import Iterator

from log_analyser.io.base import Strategy, IOContext


class InputParserStrategy(Strategy):
    def parse(self, file_path: Path) -> Iterator:
        raise NotImplementedError


class InputParser(IOContext):
    _selected_strategy: InputParserStrategy

    def parse(self, file_path: Path) -> Iterator:
        return self._selected_strategy.parse(file_path)
