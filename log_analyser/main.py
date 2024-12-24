import asyncio
import logging
import sys
from pathlib import Path
from typing import Annotated, List

import typer

from log_analyser.analyser import LogsAnalyser
from log_analyser.exceptions import InvalidDataFormatError
from log_analyser.io import output_writer, input_parser
from log_analyser.metrics import (
    MetricsCode,
    metrics_provider,
)
from log_analyser.validators import (
    validate_input_format,
    validate_output_format,
)

fmt = "[%(asctime)s] [%(levelname)s] %(message)s"
logging.basicConfig(
    level=logging.INFO,
    format=fmt,
    handlers=[logging.StreamHandler(stream=sys.stdout)],
)
logger = logging.getLogger(__name__)


app = typer.Typer()


@app.command()
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
        "csv",
        help="Expected format of the input files",
        callback=validate_input_format,
    ),
    output_format: str = typer.Option(
        "json",
        help="Expected format of the output file",
        callback=validate_output_format,
    ),
    most_frequent_ip: bool = typer.Option(
        False,
        f"--{MetricsCode.MOST_FREQUENT_IP}",
        help="Most frequent IP",
    ),
    least_frequent_ip: bool = typer.Option(
        False,
        f"--{MetricsCode.LEAST_FREQUENT_IP}",
        help="Least frequent IP",
    ),
    events_per_second: bool = typer.Option(
        False,
        f"--{MetricsCode.EVENTS_PER_SECOND}",
        help="Events per second",
    ),
    total_amount_of_bytes: bool = typer.Option(
        False,
        f"--{MetricsCode.TOTAL_AMOUNT_OF_BYTES}",
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
        MetricsCode.TOTAL_AMOUNT_OF_BYTES: total_amount_of_bytes,
    }

    if not any(options.values()):
        raise typer.BadParameter("No option was provided for analysis")

    try:
        logs_parsers = [
            input_parser.parse(input_file) for input_file in input_file_paths
        ]

        analyser = LogsAnalyser(logs_parsers, metrics_provider, options)
        asyncio.run(analyser.analyse())

        output_writer.write(output_file_path, analyser.summarise())

        logger.info(
            "Saved analysis summary into a file %s",
            str(output_file_path),
        )

    except (InvalidDataFormatError, NotImplementedError) as e:
        logger.error(e)


#
# if __name__ == "__main__":
#     typer.run(main)
