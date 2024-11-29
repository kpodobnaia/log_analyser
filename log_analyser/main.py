import asyncio
import logging
from pathlib import Path
from typing import Annotated, Any, List

import typer

from log_analyser.exceptions import InvalidDataFormatError
from log_analyser.io import output_writer, input_parser
from log_analyser.metrics import (
    MetricsCode,
    IPFrequencyMetric,
    EventsPerRecordMetric,
    TotalAmountOfBytesExchangedMetric,
)
from log_analyser.metrics.base import Metric

fmt = "%(message)s"
logging.basicConfig(level=logging.INFO, format=fmt)
logger = logging.getLogger(__name__)


# app = typer.Typer()


async def collect_metrics_from_logs(log_reader, metrics):
    for log in log_reader:
        for metric in metrics:
            metric.collect(log)


async def analyze_multiple_log_sources(log_readers, metrics) -> dict[str, Any]:
    """
    Analyze multiple log sources by creating a task for each of
    the `log_readers` and return their common
    :param log_readers: iterators that read lines from a selected file and
            parse them into Log objects
    :param metrics: Metrics objects that collect the statistics from all
            `log_readers` and summarize their common result
    :return:
    """
    tasks = [
        asyncio.create_task(collect_metrics_from_logs(log_reader, metrics))
        for log_reader in log_readers
    ]
    await asyncio.gather(*tasks)

    summary: dict[str, Any] = {}
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
    input_format: str = typer.Option(
        "csv", help="Expected format of the input files"
    ),
    output_format: str = typer.Option(
        "json", help="Expected format of the output file"
    ),
    most_frequent_ip: bool = typer.Option(
        False,
        f"--{MetricsCode.MOST_FREQUENT_IP}",
        is_flag=True,
        help="Most frequent IP",
    ),
    least_frequent_ip: bool = typer.Option(
        False,
        f"--{MetricsCode.LEAST_FREQUENT_IP}",
        is_flag=True,
        help="Least frequent IP",
    ),
    events_per_second: bool = typer.Option(
        False,
        f"--{MetricsCode.EVENTS_PER_SECOND}",
        is_flag=True,
        help="Events per second",
    ),
    total_amount_of_bytes_exchanged: bool = typer.Option(
        False,
        f"--{MetricsCode.TOTAL_AMOUNT_OF_BYTES_EXCHANGED}",
        is_flag=True,
        help="Total amount of bytes exchanged",
    ),
) -> None:
    """A command-line tool to analyze the content of log files.
    The tool accepts the log file location(s) and operation(s) as
    input arguments and return the results of the operations as output.
    """
    output_writer.select_strategy(output_format)
    input_parser.select_strategy(input_format)

    metrics: List[Metric] = []
    try:
        if most_frequent_ip or least_frequent_ip:
            metrics.append(IPFrequencyMetric())
        if events_per_second:
            metrics.append(EventsPerRecordMetric())
        if total_amount_of_bytes_exchanged:
            metrics.append(TotalAmountOfBytesExchangedMetric())

        if not metrics:
            logger.error("No option was provided for analysis")
            raise typer.Exit()

        logs_parsers = [
            input_parser.parse(input_file) for input_file in input_file_paths
        ]
        summary = asyncio.run(
            analyze_multiple_log_sources(logs_parsers, metrics)
        )

        output_writer.write(output_file_path, summary)

    except (InvalidDataFormatError, NotImplementedError) as e:
        logger.error(e)

    logger.info("Finished.")


if __name__ == "__main__":
    typer.run(main)
