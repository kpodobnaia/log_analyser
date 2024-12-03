import json

import pytest
from typer.testing import CliRunner

from log_analyser.main import app
from tests.utils import clean_stdout_content

runner = CliRunner()

SUCCESS = 0
ABORTED = 1
VALIDATION_ERR = 2


@pytest.mark.parametrize(
    ("input_paths", "options", "expected_result"),
    [
        (
            [
                "valid_csv_1.log",
                "valid_csv_2.log",
            ],
            ["mfip", "lfip", "eps", "bytes"],
            {
                "mfip": "10.105.21.199",
                "lfip": "10.105.37.17",
                "eps": 0.6382978723404256,
                "bytes": 185388,
            },
        ),
        (
            ["valid_csv_2.log"],
            ["mfip", "lfip", "eps", "bytes"],
            {
                "mfip": "10.105.33.214",
                "lfip": "10.105.21.199",
                "eps": 2.0,
                "bytes": 111987,
            },
        ),
        (
            ["valid_csv_2.log"],
            ["lfip"],
            {
                "lfip": "10.105.21.199",
            },
        ),
    ],
)
def test_log_analyser_no_error(
    input_paths, options, expected_result, tmp_path, data_path
):
    output_path = str(tmp_path / "output.json")
    input_full_paths = [
        str(data_path / file_path) for file_path in input_paths
    ]

    result = runner.invoke(
        app,
        [*input_full_paths, output_path, *(f"--{o}" for o in options)],
    )
    assert result.exit_code == SUCCESS

    with open(output_path, "r") as f:
        assert json.loads(f.read()) == expected_result


def test_log_analyser_incorrect_input_paths(tmp_path):
    output_path = str(tmp_path / "output.json")
    result = runner.invoke(
        app,
        [
            "invalid_input_path.log",
            output_path,
            "--mfip",
        ],
    )
    assert result.exit_code == VALIDATION_ERR

    assert (
        "Invalid value for INPUT_FILE_PATHS... "
        "Path invalid_input_path.log does not exist."
        in clean_stdout_content(result.stdout)
    )


def test_log_analyser_no_metric_options(tmp_path, data_path):
    input_path = str(data_path / "valid_csv_1.log")
    output_path = str(tmp_path / "output.json")

    result = runner.invoke(
        app,
        [input_path, output_path],
    )
    assert result.exit_code == VALIDATION_ERR
    assert (
        "Error Invalid value No option was provided for analysis"
        in clean_stdout_content(result.stdout)
    )


def test_log_analyser_unsupported_input_format(tmp_path, data_path):
    input_path = str(data_path / "valid_csv_1.log")
    output_path = str(tmp_path / "output.json")

    result = runner.invoke(
        app,
        [
            input_path,
            output_path,
            "--mfip",
            "--input-format",
            "test",
        ],
    )
    assert result.exit_code == VALIDATION_ERR
    assert (
        "Invalid value for input format Input format test is not supported."
        in clean_stdout_content(result.stdout)
    )


def test_log_analyser_unsupported_output_format(tmp_path, data_path):
    input_path = str(data_path / "valid_csv_1.log")
    output_path = str(tmp_path / "output.json")

    result = runner.invoke(
        app,
        [
            input_path,
            output_path,
            "--mfip",
            "--output-format",
            "test",
        ],
    )
    assert result.exit_code == VALIDATION_ERR
    assert (
        "Invalid value for output format Output format test is not supported."
        in clean_stdout_content(result.stdout)
    )
