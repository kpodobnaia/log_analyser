import abc
from typing import Any, Type

from log_analyser.log import LogEntry


class Metric(abc.ABC):
    def collect(self, log: LogEntry) -> None:
        raise NotImplementedError

    def summarize(self) -> Any:
        raise NotImplementedError


class MetricsProvider:
    def __init__(self):
        self._available_metrics: dict[str, Type[Metric]] = {}

    def register(self, code: str, metric: Type[Metric]) -> None:
        self._available_metrics[code] = metric

    def provide_metrics(self, codes: list[str]) -> list[Metric]:
        unique_metric_classes = {
            self._available_metrics[code] for code in codes
        }
        return [metric() for metric in unique_metric_classes]
