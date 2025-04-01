from typing import Any

from log_analyser.log_entry import LogEntry
from log_analyser.metrics.base import Metric


class TotalAmountOfBytesExchangedMetric(Metric):
    """
    Total amount of bytes exchanged is the metric that takes into response
    size in bytes.
    """

    def __init__(self):
        self._total_amount = 0

    def collect(self, log: LogEntry) -> None:
        self._total_amount += log.response_size_in_bytes

    def summarize(self) -> dict[str, Any]:
        if self._total_amount == 0:
            return {}

        return {"bytes": self._total_amount}
