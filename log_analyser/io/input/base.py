from pathlib import Path

from log_analyser.io.base import Strategy, IOContext


class InputParserStrategy(Strategy):
    def parse(self, file_path: Path) -> None:
        raise NotImplementedError


class InputParser(IOContext):
    _selected_strategy: InputParserStrategy

    def parse(self, file_path: Path) -> None:
        self._selected_strategy.parse(file_path)
