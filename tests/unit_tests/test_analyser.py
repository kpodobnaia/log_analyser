from unittest.mock import MagicMock

import pytest

from log_analyser.analyser import LogsAnalyser


@pytest.fixture
def log_parsers():
    return [(MagicMock() for _ in range(10))]


@pytest.fixture
def metric1():
    metric = MagicMock()
    metric.return_value.summary = {"a": 10}
    return metric


@pytest.fixture
def metric2():
    metric = MagicMock()
    metric.return_value.summary = {"b": 5}
    return metric


@pytest.fixture
def metrics_provider(metric1):
    provider = MagicMock()

    provider.return_value.provide_metrics.return_value = [
        metric1,
    ]
    return provider


@pytest.mark.asyncio
async def test_analyse_no_error(
    log_parsers, metrics_provider, metric1, metric2
):
    analyser = LogsAnalyser(
        log_parsers, metrics_provider, options={"a": True, "b": False}
    )
    await analyser.analyse()

    assert metric1.return_value.collect.call_count == 10
    metric2.return_value.collect.assert_not_called()

    assert analyser.summarise() == {"a": 10}

    assert metric1.return_value.summarise.call_count.called_once()
    metric2.return_value.summarise.assert_not_called()


def test_analyse_no_parsers():
    log_parsers = []
    analyser = LogsAnalyser()


def test_analyse_no_metrics():
    pass
