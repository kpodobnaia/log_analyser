import logging
import os
import sys

log_level = os.environ.get('LOG_LEVEL') or logging.INFO
fmt = "[%(asctime)s] [%(levelname)s] %(message)s"

logging.basicConfig(
    level=log_level,
    format=fmt,
    handlers=[logging.StreamHandler(stream=sys.stdout)],
)
