from datetime import datetime
from typing import Any

from log_analyser.log import LogEntry
from log_analyser.metrics.base import Metric


class EventsPerRecordMetric(Metric):
    """
    EPS is determined by dividing the total number of events generated within
    a specific time period by the duration of that time period.
    """

    def __init__(self):
        self._start_timestamp = datetime.now()
        self._end_timestamp = datetime.fromtimestamp(0)
        self._events_count = 0

    def collect(self, log: LogEntry) -> None:
        if log.timestamp < self._start_timestamp:
            self._start_timestamp = log.timestamp

        if log.timestamp > self._end_timestamp:
            self._end_timestamp = log.timestamp

        self._events_count += 1

    def summarize(self) -> dict[str, Any]:
        time_interval = (self._end_timestamp - self._start_timestamp).seconds

        if time_interval == 0 or self._events_count == 0:
            return {}

        result = self._events_count / time_interval
        return {"eps": result}
