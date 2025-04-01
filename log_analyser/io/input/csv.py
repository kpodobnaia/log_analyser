import csv
from datetime import datetime
from pathlib import Path
from typing import Iterator, TextIO

from log_analyser.exceptions import InvalidDataFormatError
from log_analyser.io.input.base import InputParserStrategy
from log_analyser.log_entry import LogEntry
from log_analyser.logging import logging

logger = logging.getLogger(__name__)


class CSVInputParserStrategy(InputParserStrategy):
    POSSIBLE_DELIMITERS = [" ", ";", ",", "\t"]
    EXPECTED_NUMBER_OF_COLUMNS = 10

    def parse(self, file_path: Path) -> Iterator:
        rows_count = 0
        skipped_rows_count = 0

        with file_path.open("r+t") as f:
            reader = self._get_csv_reader(f)
            for row in reader:
                rows_count += 1

                if not row:
                    skipped_rows_count += 1
                    continue

                try:
                    yield self._parse_csv_row(row)
                except Exception as e:
                    skipped_rows_count += 1
                    msg = "Could not parse a line from CSV %s. Skipping. %s"
                    logger.warning(msg, file_path, str(e))
                    continue
            logger.info(
                "Processed %s/%s rows in %s.",
                rows_count - skipped_rows_count,
                rows_count,
                file_path,
            )

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

    def _get_csv_reader(self, file: TextIO):
        for delimiter in self.POSSIBLE_DELIMITERS:
            file.seek(0)
            reader = csv.reader(
                file, delimiter=delimiter, skipinitialspace=True
            )

            for row in reader:

                if not row:
                    continue

                if len(row) < self.EXPECTED_NUMBER_OF_COLUMNS:
                    break

                file.seek(0)
                return csv.reader(
                    file, delimiter=delimiter, skipinitialspace=True
                )

        raise InvalidDataFormatError("The data is not in CSV format.")
