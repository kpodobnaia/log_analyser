from typer.testing import CliRunner

from log_analyser.main import app
from tests.conftest import VALIDATION_ERR
from tests.utils import clean_stdout_content

runner = CliRunner()


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


def test_log_analyser_no_input_path(tmp_path, data_path):
    output_path = str(tmp_path / "output.json")

    result = runner.invoke(
        app,
        [
            output_path,
            "--mfip",
        ],
    )
    assert result.exit_code == VALIDATION_ERR
    assert "Error Missing argument INPUT_FILE_PATHS" in clean_stdout_content(
        result.stdout
    )


def test_log_analyser_no_input_does_not_exist(tmp_path, data_path):
    input_path = str(data_path / "invalid.log")
    output_path = str(tmp_path / "output.json")

    result = runner.invoke(
        app,
        [
            input_path,
            output_path,
            "--mfip",
        ],
    )
    assert result.exit_code == VALIDATION_ERR
    assert "Error Invalid value for INPUT_FILE_PATHS" in clean_stdout_content(
        result.stdout
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


def test_log_analyser_no_output_path(data_path):
    input_path = str(data_path / "valid_csv_1.log")

    result = runner.invoke(app, [input_path, "--mfip"])

    assert result.exit_code == VALIDATION_ERR

    # the error message is strange
    assert "Error Missing argument INPUT_FILE_PATHS" in clean_stdout_content(
        result.stdout
    )
