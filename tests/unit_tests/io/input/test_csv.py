from datetime import datetime
from unittest.mock import MagicMock, patch

import pytest

from log_analyser.io.input.csv import CSVInputParserStrategy
from log_analyser.log import LogEntry


@patch("csv.reader")
def test_csv_log_parser_parses_data_correctly(mock_csv_reader):
    test_data = [
        [],
        [
            "1157689312.049",
            "5006",
            "10.100.11.199",
            "TCP_MISS/200",
            "19763",
            "CONNECT",
            "login.test.com:443",
            "user",
            "DIRECT/100.11.111.115",
            "-",
        ],
        [
            "1157689325.734",
            "1452",
            "10.100.11.100",
            "TCP_REFRESH_HIT/304",
            "214",
            "GET",
            "http://www.test.com/flags/FUS.gif",
            "user",
            "DIRECT/100.11.111.61",
            "",
        ],
    ]
    mocked_path = MagicMock()
    mock_csv_reader.return_value = iter(test_data)

    logs_parser = CSVInputParserStrategy().parse(mocked_path)

    result = next(logs_parser)
    assert result == LogEntry(
        timestamp=datetime(2006, 9, 8, 6, 21, 52, 49000),
        response_header_size_in_bytes=5006,
        client_ip_address="10.100.11.199",
        http_response_code="TCP_MISS/200",
        response_size_in_bytes=19763,
        http_request_method="CONNECT",
        url="login.test.com:443",
        username="user",
        tipe_of_access="DIRECT",
        destination_ip_address="100.11.111.115",
        response_type="-",
    )

    result = next(logs_parser)
    assert result == LogEntry(
        timestamp=datetime(2006, 9, 8, 6, 22, 5, 734000),
        response_header_size_in_bytes=1452,
        client_ip_address="10.100.11.100",
        http_response_code="TCP_REFRESH_HIT/304",
        response_size_in_bytes=214,
        http_request_method="GET",
        url="http://www.test.com/flags/FUS.gif",
        username="user",
        tipe_of_access="DIRECT",
        destination_ip_address="100.11.111.61",
        response_type="",
    )

    with pytest.raises(StopIteration):
        next(logs_parser)


@patch("csv.reader")
@patch("log_analyser.io.input.csv.logger")
def test_csv_log_parser_with_invalid_data(mock_logger, mock_csv_reader):
    test_data = [
        [],
        [
            "not_a_date",
            "5006",
            "10.100.11.199",
            "TCP_MISS/200",
            "19763",
            "CONNECT",
            "login.test.com:443",
            "user",
            "DIRECT/100.11.111.115",
            "-",
        ],
        [
            "1157689325.734",
            "5006",
            "10.100.11.199",
            "TCP_MISS/200",
            "19763",
            "CONNECT",
            "login.test.com:443",
        ],
    ]
    mocked_path = MagicMock()
    mock_csv_reader.return_value = iter(test_data)

    logs_parser = CSVInputParserStrategy().parse(mocked_path)

    with pytest.raises(StopIteration):
        next(logs_parser)

    assert mock_logger.warning.call_count == 2
