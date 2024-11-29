import csv
import logging
from datetime import datetime
from pathlib import Path
from typing import Iterator

from log_analyser.io.input.base import InputParserStrategy
from log_analyser.log import LogEntry

logger = logging.getLogger(__name__)


class CSVInputParserStrategy(InputParserStrategy):
    def parse(self, file_path: Path) -> Iterator:
        with file_path.open("r+t") as f:
            reader = csv.reader(f, delimiter=" ", skipinitialspace=True)
            for row in reader:
                if not row:
                    continue
                try:
                    yield self._parse_csv_row(row)
                except Exception as e:
                    msg = "Could not parse a line from CSV. Skipping. %s %s"
                    logger.warning(msg, file_path, str(e))
                    continue

    @staticmethod
    def _parse_csv_row(fields: list[str]) -> LogEntry:
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
