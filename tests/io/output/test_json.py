from unittest.mock import MagicMock

import pytest

from log_analyser.exceptions import InvalidDataFormatError
from log_analyser.io.output.json import JSONOutputWriterStrategy


def test_json_strategy():
    json_writer = JSONOutputWriterStrategy()
    path = MagicMock()
    json_writer.write(path, content={"test": "sample"})

    path.write_text.assert_called_with('{"test": "sample"}')


def test_json_strategy_with_binary():
    json_writer = JSONOutputWriterStrategy()
    path = MagicMock()

    with pytest.raises(InvalidDataFormatError):
        json_writer.write(path, content=b"incorrect")
