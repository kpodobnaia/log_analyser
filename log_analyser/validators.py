import typer

from log_analyser.io import input_parser, output_writer


def validate_input_format(input_format: str):
    if input_format not in input_parser.supported_formats:
        raise typer.BadParameter(
            f"Input format {input_format} is not supported."
        )
    return input_format


def validate_output_format(output_format: str):
    if output_format not in output_writer.supported_formats:
        raise typer.BadParameter(
            f"Output format {output_format} is not supported."
        )
    return output_format
