from collections import Counter
from typing import Any

from log_analyser.log_entry import LogEntry
from log_analyser.metrics.base import Metric
from log_analyser.metrics.metrics_codes import MetricsCode


class IPFrequencyMetric(Metric):
    def __init__(self):
        self._counter = Counter()

    def collect(self, log: LogEntry) -> None:
        self._counter[log.client_ip_address] += 1

    def summarize(self) -> dict[str, Any]:
        most_common = self._counter.most_common()

        if not most_common:
            return {}

        return {
            MetricsCode.MOST_FREQUENT_IP: most_common[0][0],
            MetricsCode.LEAST_FREQUENT_IP: most_common[-1][0],
        }
