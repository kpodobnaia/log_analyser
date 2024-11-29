import abc


class Strategy(abc.ABC):
    pass


class IOContext(abc.ABC):
    _registry: dict[str, Strategy] = {}
    _selected_strategy: Strategy

    def register(self, file_format: str, strategy: Strategy) -> None:
        self._registry[file_format] = strategy

    def select_strategy(self, file_format) -> None:
        if file_format not in self._registry:
            raise NotImplementedError

        self._selected_strategy = self._registry[file_format]
