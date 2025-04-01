import json
from pathlib import Path
from typing import Any

from log_analyser.exceptions import InvalidDataFormatError
from log_analyser.io.output.base import OutputWriterStrategy
from log_analyser.logging import logging

logger = logging.getLogger(__name__)


class JSONOutputWriterStrategy(OutputWriterStrategy):
    def write(self, file_path: Path, content: Any) -> None:
        if not content:
            logger.info(
                "There is no content to save to %s.",
                file_path,
            )
            return
        try:
            file_path.write_text(json.dumps(content))
            logger.info(
                "Saved analysis summary into a file %s",
                str(file_path),
            )
        except Exception as e:
            raise InvalidDataFormatError(
                f"Could not save data to a file "
                f"{file_path.absolute()}. {str(e)}"
            )
