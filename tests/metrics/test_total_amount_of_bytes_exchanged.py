from unittest.mock import MagicMock

from log_analyser.metrics import TotalAmountOfBytesExchangedMetric, MetricsCode


def test_total_amount_of_bytes_exchanged():
    metric = TotalAmountOfBytesExchangedMetric()
    sizes = [123, 1234, 456, 2456, 3235]

    for size in sizes:
        metric.collect(MagicMock(response_size_in_bytes=size))

    assert metric.summarize() == {
        MetricsCode.TOTAL_AMOUNT_OF_BYTES_EXCHANGED: sum(sizes)
    }


def test_total_amount_of_bytes_exchanged_empty():
    metric = TotalAmountOfBytesExchangedMetric()

    assert metric.summarize() == {}
