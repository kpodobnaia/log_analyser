from .base import MetricsProvider
from .events_per_second import EventsPerSecondMetric
from .ip_frequency import IPFrequencyMetric
from .metrics_codes import MetricsCode
from .total_amount_of_bytes_exchanged import TotalAmountOfBytesExchangedMetric

metrics_provider = MetricsProvider()
metrics_provider.register(MetricsCode.MOST_FREQUENT_IP, IPFrequencyMetric)
metrics_provider.register(MetricsCode.LEAST_FREQUENT_IP, IPFrequencyMetric)
metrics_provider.register(MetricsCode.EVENTS_PER_SECOND, EventsPerSecondMetric)
metrics_provider.register(
    MetricsCode.TOTAL_AMOUNT_OF_BYTES_EXCHANGED,
    TotalAmountOfBytesExchangedMetric,
)

__all__ = ["MetricsCode", "metrics_provider"]
