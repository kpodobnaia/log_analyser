import asyncio
from typing import Any, Iterator, List, Dict

from log_analyser.log import LogEntry
from log_analyser.metrics.base import MetricsProvider


class LogsAnalyser:
    def __init__(
        self,
        log_parsers: List[Iterator[LogEntry]],
        metrics_provider: MetricsProvider,
        options: Dict[str, bool],
    ) -> None:
        self._log_parsers = log_parsers
        self._included_options = [
            key for key, enabled in options.items() if enabled
        ]
        self._metrics = metrics_provider.provide_metrics(
            self._included_options
        )

    async def analyse(self) -> None:
        """
        Analyse multiple logs from multiple sources by creating a task for
        each of the log parsers (iterators) and accumulate metrics inside
        `self._metrics`.
        """
        tasks = [
            asyncio.create_task(self._collect_metrics_from_logs(log_reader))
            for log_reader in self._log_parsers
        ]
        await asyncio.gather(*tasks)

    def summarise(self) -> Dict[str, Any]:
        """
        Prepare summary for collected metrics for logs from all sources. Filter
        results for options that are not included by a user (as a trade-off
        for allowing to process multiple options by the same metric)
        :return: summary from each selected metric
        """
        summary: dict[str, Any] = {}

        for metric in self._metrics:
            summary |= metric.summarize()

        filtered_summary: dict[str, Any] = {
            key: value
            for key, value in summary.items()
            if key in self._included_options
        }
        return filtered_summary

    async def _collect_metrics_from_logs(
        self, log_reader: Iterator[LogEntry]
    ) -> None:
        for log in log_reader:
            for metric in self._metrics:
                metric.collect(log)
