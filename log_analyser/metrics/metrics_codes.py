from enum import StrEnum


class MetricsCode(StrEnum):
    MOST_FREQUENT_IP = "mfip"
    LEAST_FREQUENT_IP = "lfip"
    EVENTS_PER_SECOND = "eps"
    TOTAL_AMOUNT_OF_BYTES_EXCHANGED = "bytes"
