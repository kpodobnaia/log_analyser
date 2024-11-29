import abc
from typing import Any

from log_analyser.log import LogEntry


class Metric(abc.ABC):
    def collect(self, log: LogEntry) -> None:
        raise NotImplemented

    def summarize(self) -> Any:
        raise NotImplemented
