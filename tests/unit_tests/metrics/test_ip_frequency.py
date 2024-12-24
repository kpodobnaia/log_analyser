from unittest.mock import MagicMock

from log_analyser.metrics import IPFrequencyMetric, MetricsCode


def test_ip_frequency():
    metric = IPFrequencyMetric()

    metric.collect(MagicMock(client_ip_address="1.2.3.4"))
    metric.collect(MagicMock(client_ip_address="1.2.3.5"))
    metric.collect(MagicMock(client_ip_address="1.2.3.4"))
    metric.collect(MagicMock(client_ip_address="1.2.3.4"))
    metric.collect(MagicMock(client_ip_address="1.2.3.3"))
    metric.collect(MagicMock(client_ip_address="1.2.3.3"))

    assert metric.summarize() == {
        MetricsCode.LEAST_FREQUENT_IP: "1.2.3.5",
        MetricsCode.MOST_FREQUENT_IP: "1.2.3.4",
    }


def test_ip_frequency_empty():
    metric = IPFrequencyMetric()

    assert metric.summarize() == {}
