import asyncio
import logging
import sys
from pathlib import Path
from typing import Annotated, Any, List

import typer

from log_analyser.exceptions import InvalidDataFormatError
from log_analyser.io import output_writer, input_parser
from log_analyser.metrics import (
    MetricsCode,
    metrics_provider,
)

fmt = "[%(asctime)s] [%(levelname)s] %(message)s"
logging.basicConfig(
    level=logging.INFO,
    format=fmt,
    handlers=[logging.StreamHandler(stream=sys.stdout)],
)
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


async def analyser(
    logs_parsers, output_writer, output_file_path, metrics, options
):
    summary = await analyze_multiple_log_sources(logs_parsers, metrics)

    # trade-off for allowing to process multiple options by the same metric
    filtered_summary = {
        key: value
        for key, value in summary.items()
        if key in options and options[key]
    }

    output_writer.write(output_file_path, filtered_summary)
    logger.info(
        "Saved analysis summary into a file %s",
        str(output_file_path),
    )


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
    total_amount_of_bytes: bool = typer.Option(
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
    logger.info(
        "Start analysing logs in files: %s",
        ", ".join([str(f) for f in input_file_paths]),
    )
    output_writer.select_strategy(output_format)
    input_parser.select_strategy(input_format)

    options = {
        MetricsCode.MOST_FREQUENT_IP: most_frequent_ip,
        MetricsCode.LEAST_FREQUENT_IP: least_frequent_ip,
        MetricsCode.EVENTS_PER_SECOND: events_per_second,
        MetricsCode.TOTAL_AMOUNT_OF_BYTES_EXCHANGED: total_amount_of_bytes,
    }

    if not any(options.values()):
        logger.error("No option was provided for analysis")
        raise typer.Exit()

    try:
        metrics = metrics_provider.provide_metrics(
            [option for option, enabled in options.items() if enabled]
        )

        logs_parsers = [
            input_parser.parse(input_file) for input_file in input_file_paths
        ]
        asyncio.run(
            analyser(
                logs_parsers, output_writer, output_file_path, metrics, options
            )
        )

    except (InvalidDataFormatError, NotImplementedError) as e:
        logger.error(e)


if __name__ == "__main__":
    typer.run(main)
