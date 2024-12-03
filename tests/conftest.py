from pathlib import Path

import pytest

TEST_DATA_DIR = Path(__file__).parent / "testdata/"


@pytest.fixture
def data_path():
    return TEST_DATA_DIR
