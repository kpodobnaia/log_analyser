from pathlib import Path

from typer.testing import CliRunner

from log_analyser.main import app

runner = CliRunner()


def test_log_analyser_other_csv_delimiter(tmp_path, data_path, caplog):
    input_path = str(data_path / "mixedup_missing_data.log")
    output_path = str(tmp_path / "output.json")

    result = runner.invoke(
        app,
        [input_path, output_path, "--mfip"],
    )

    assert result.exit_code == 0
    assert not Path(output_path).exists()
    assert result.stdout == ""

    for record in caplog.records:
        assert record.levelname == "WARNING"
        expected_message = f"Could not parse a line from CSV {input_path}. Skipping. list index out of range"
        assert record.message == expected_message
