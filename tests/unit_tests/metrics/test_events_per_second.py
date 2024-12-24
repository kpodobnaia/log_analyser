from datetime import datetime, timedelta
from unittest.mock import MagicMock

from log_analyser.metrics import MetricsCode
from log_analyser.metrics.events_per_second import EventsPerSecondMetric


def test_events_per_second():
    now = datetime.now()
    metric = EventsPerSecondMetric()

    metric.collect(MagicMock(timestamp=now))
    metric.collect(MagicMock(timestamp=now))
    metric.collect(MagicMock(timestamp=now + timedelta(seconds=2)))
    metric.collect(MagicMock(timestamp=now + timedelta(seconds=4)))
    metric.collect(MagicMock(timestamp=now + timedelta(seconds=5)))
    metric.collect(MagicMock(timestamp=now + timedelta(seconds=5)))
    metric.collect(MagicMock(timestamp=now + timedelta(seconds=5)))

    # check how big time interval is in seconds
    assert (now - now + timedelta(seconds=5)).seconds == 5

    assert metric.summarize() == {MetricsCode.EVENTS_PER_SECOND: 1.4}


def test_events_per_second_empty():
    metric = EventsPerSecondMetric()

    assert metric.summarize() == {}
