import abc
from collections import Counter
from datetime import datetime
from enum import Enum
from typing import Any

from log_analyser.log import LogEntry


class MetricsCode(Enum):
    MOST_FREQUENT_IP = "mfip"
    LEAST_FREQUENT_IP = "lfip"
    EVENTS_PER_SECOND = "eps"
    TOTAL_AMOUNT_OF_BYTES_EXCHANGED = "bytes"


class Metrics(abc.ABC):
    def collect(self, log: LogEntry) -> None:
        raise NotImplemented

    def summarize(self) -> Any:
        raise NotImplemented


class IPFrequencyMetrics(Metrics):
    def __init__(self):
        self.counter = Counter()

    def collect(self, log: LogEntry) -> None:
        self.counter[log.client_ip_address] += 1

    def summarize(self) -> dict[str, Any]:
        most_common = self.counter.most_common()
        return {
            MetricsCode.MOST_FREQUENT_IP.value: most_common[0],
            MetricsCode.LEAST_FREQUENT_IP.value: most_common[-1],
        }


class EventsPerRecordMetrics(Metrics):
    start_timestamp: datetime
    end_timestamp: datetime
    events_count: int

    def collect(self, log: LogEntry) -> None:
        pass

    def summarize(self) -> dict[str, Any]:
        pass


class TotalAmountOfBytesExchanged(Metrics):
    bytes_amount: int

    def collect(self, log: LogEntry) -> None:
        pass

    def summarize(self) -> dict[str, Any]:
        pass
