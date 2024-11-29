import json
from pathlib import Path
from typing import Any

from log_analyser.exceptions import InvalidDataFormatError
from log_analyser.io.output.base import OutputWriterStrategy


class JSONOutputWriterStrategy(OutputWriterStrategy):
    def write(self, file_path: Path, content: Any) -> None:
        try:
            file_path.write_text(json.dumps(content))
        except Exception as e:
            raise InvalidDataFormatError(f"Could not save data to a file {file_path.absolute()}. {str(e)}")
