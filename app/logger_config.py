import logging
import os
from logzio.handler import LogzioHandler

def get_logger():
    logger = logging.getLogger("weather-logger")
    logger.setLevel(logging.INFO)
    logzio_token = os.getenv("LOGZ_TOKEN")
    logzio_url = os.getenv("LOGZ_URL", "https://listener.logz.io:8071")

    logzio_handler = LogzioHandler(
        token=logzio_token,
        url=logzio_url,
        debug=True
    )
    logger.addHandler(logzio_handler)
    return logger