import json

import pytest
from typer.testing import CliRunner

from log_analyser.main import app
from tests.conftest import SUCCESS

runner = CliRunner()


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
def test_log_analyser_creates_file_with_analysis_summary(
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


def test_log_analyser_other_csv_delimiter(tmp_path, data_path):
    input_path = str(data_path / "other_csv_delimiter.log")
    output_path = str(tmp_path / "output.json")

    result = runner.invoke(
        app,
        [input_path, output_path, "--mfip"],
    )

    assert result.exit_code == 0

    with open(output_path, "r") as f:
        assert json.loads(f.read()) == {"mfip": "10.105.21.199"}
