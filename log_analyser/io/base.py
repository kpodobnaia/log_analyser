import abc
from typing import Type


class Strategy(abc.ABC):
    pass


class IOContext(abc.ABC):
    _registry: dict[str, Type[Strategy]] = {}
    _selected_strategy: Strategy
    NOT_IMPLEMENTED_MESSAGE = "Unknown format {file_format}"

    def register(self, file_format: str, strategy: Type[Strategy]) -> None:
        self._registry[file_format] = strategy

    def select_strategy(self, file_format: str) -> None:
        if file_format not in self.supported_formats:
            raise NotImplementedError(
                self.NOT_IMPLEMENTED_MESSAGE.format(file_format)
            )

        self._selected_strategy = self._registry[file_format]()

    @property
    def supported_formats(self):
        return self._registry.keys()
