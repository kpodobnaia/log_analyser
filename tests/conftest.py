from pathlib import Path

import pytest

SUCCESS = 0
ABORTED = 1
VALIDATION_ERR = 2

TEST_DATA_DIR = Path(__file__).parent / "testdata/"


@pytest.fixture
def data_path():
    return TEST_DATA_DIR
