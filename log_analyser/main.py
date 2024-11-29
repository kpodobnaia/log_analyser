import asyncio
import logging
from pathlib import Path
from typing import Annotated, Any, List

import typer

from log_analyser.metrics import (
    MetricsCode,
    IPFrequencyMetrics,
    EventsPerRecordMetrics,
    TotalAmountOfBytesExchanged,
)
from log_analyser.readers import get_file_reader
from log_analyser.writers import get_file_writer

fmt = "%(message)s"
logging.basicConfig(level=logging.INFO, format=fmt)
logger = logging.getLogger(__name__)


# app = typer.Typer()


async def collect_metrics_from_logs(log_reader, metrics) -> dict[str, Any]:
    for log in log_reader:
        for metric in metrics:
            metric.collect(log)


async def analyze_multiple_log_sources(log_readers, metrics) -> dict[str, Any]:
    """
    Analyze multiple log sources by creating a task for each of the `log_readers` and return their common
    :param log_readers: iterators that read lines from a selected file and parse them into Log objects
    :param metrics: Metrics objects that collect the statistics from all `log_readers` and summarize their common result
    :return:
    """
    tasks = [
        asyncio.create_task(collect_metrics_from_logs(log_reader, metrics))
        for log_reader in log_readers
    ]
    await asyncio.gather(*tasks)

    summary = {}
    # metric objects accumulate the statistics for logs from all sources
    for metric in metrics:
        summary |= metric.summarize()
    return summary


# @app.command()
def main(
    input_file_paths: Annotated[
        List[Path],
        typer.Argument(
            default=...,
            show_default=False,
            exists=True,
            readable=True,
            resolve_path=True,
            help="Path to one or more input files",
        ),
    ],
    output_file_path: Annotated[
        Path,
        typer.Argument(
            default=...,
            show_default=False,
            writable=True,
            help="Path to a file to save output in plain text",
        ),
    ],
    input_format: str = typer.Option("csv", help="Expected format of the input files"),
    output_format: str = typer.Option(
        "json", help="Expected format of the output file"
    ),
    most_frequent_ip: bool = typer.Option(
        False,
        f"--{MetricsCode.MOST_FREQUENT_IP.value}",
        is_flag=True,
        help="Most frequent IP",
    ),
    least_frequent_ip: bool = typer.Option(
        False,
        f"--{MetricsCode.LEAST_FREQUENT_IP.value}",
        is_flag=True,
        help="Least frequent IP",
    ),
    events_per_second: bool = typer.Option(
        False,
        f"--{MetricsCode.EVENTS_PER_SECOND.value}",
        is_flag=True,
        help="Events per second",
    ),
    total_amount_of_bytes_exchanged: bool = typer.Option(
        False,
        f"--{MetricsCode.TOTAL_AMOUNT_OF_BYTES_EXCHANGED.value}",
        is_flag=True,
        help="Total amount of bytes exchanged",
    ),
) -> None:
    """A command-line tool to analyze the content of log files. The tool accepts the log file
    location(s) and operation(s) as input arguments and return the results of the operations as output.
    """
    metrics = []
    try:
        if most_frequent_ip or least_frequent_ip:
            metrics.append(IPFrequencyMetrics())
        if events_per_second:
            metrics.append(EventsPerRecordMetrics())
        if total_amount_of_bytes_exchanged:
            metrics.append(TotalAmountOfBytesExchanged())

        if not metrics:
            logger.error("No option was provided for analysis")
            raise typer.Exit()

        file_reader = get_file_reader(input_format)
        logs_readers = [file_reader(input_file) for input_file in input_file_paths]
        summary = asyncio.run(analyze_multiple_log_sources(logs_readers, metrics))
        summary_writer = get_file_writer(output_format)(output_file_path)
        summary_writer(summary)

    except NotImplementedError as e:
        logger.error(e)

    logger.info("Finished.")


if __name__ == "__main__":
    typer.run(main)
