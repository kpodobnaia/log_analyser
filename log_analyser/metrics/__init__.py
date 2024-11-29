from .base import MetricsProvider
from .events_per_second import EventsPerRecordMetric
from .ip_frequency import IPFrequencyMetric
from .metrics_codes import MetricsCode
from .total_amount_of_bytes_exchanged import TotalAmountOfBytesExchangedMetric

metrics_provider = MetricsProvider()
metrics_provider.register("mfit", IPFrequencyMetric)
metrics_provider.register("lfit", IPFrequencyMetric)
metrics_provider.register("eps", EventsPerRecordMetric)
metrics_provider.register("bytes", TotalAmountOfBytesExchangedMetric)

__all__ = ["MetricsCode", "metrics_provider"]
