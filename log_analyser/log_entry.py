from dataclasses import dataclass
from datetime import datetime


@dataclass
class LogEntry:
    timestamp: datetime
    response_header_size_in_bytes: int
    client_ip_address: str
    http_response_code: str
    response_size_in_bytes: int
    http_request_method: str
    url: str
    username: str
    tipe_of_access: str
    destination_ip_address: str
    response_type: str
