import csv
from datetime import datetime
from pathlib import Path

from log_analyser.log import LogEntry
from log_analyser.readers.registry import register_reader


def parse_csv_row(fields: list[str]) -> LogEntry:
    tipe_of_access, destination_ip_address = fields[8].split("/")
    return LogEntry(
        timestamp=datetime.fromtimestamp(float(fields[0])),
        response_header_size_in_bytes=int(fields[1]),
        client_ip_address=fields[2],
        http_response_code=fields[3],
        response_size_in_bytes=int(fields[4]),
        http_request_method=fields[5],
        url=fields[6],
        username=fields[7],
        tipe_of_access=tipe_of_access,
        destination_ip_address=destination_ip_address,
        response_type=fields[9],
    )


@register_reader("csv")
def csv_reader(file_path: Path):
    with open(file_path) as f:
        reader = csv.reader(f, delimiter=" ", skipinitialspace=True)
        for row in reader:
            if not row:
                continue
            try:
                yield parse_csv_row(row)
            except Exception:
                continue
