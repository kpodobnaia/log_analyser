import abc
from typing import Any

from log_analyser.log import LogEntry


class Metric(abc.ABC):
    def collect(self, log: LogEntry) -> None:
        raise NotImplementedError

    def summarize(self) -> Any:
        raise NotImplementedError
