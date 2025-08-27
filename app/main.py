import os
import sys
import time
import signal
import json
import requests
from typing import List

from logger_config import get_logger
from sources.openweathermap import OpenWeatherMapSource
from sources.weatherapi import WeatherAPISource
from sources.csv_source import CSVSource
from models.weather import WeatherData


# Global flag for graceful shutdown
RUNNING = True


def signal_handler(sig, frame):
    global RUNNING
    print("Shutdown signal received, finishing last cycle...")
    RUNNING = False


def load_sources(logger):
    """Initialize sources based on environment variables."""
    sources = []

    data_sources = os.getenv("DATA_SOURCES", "owm,wapi,file").split(",")

    if "owm" in data_sources:
        try:
            cities = os.getenv("OWM_CITIES", "").split(",")
            if not cities or cities == [""]:
                raise ValueError("OWM_CITIES not configured")
            sources.append(OpenWeatherMapSource(cities))
            logger.info(f"Configured OpenWeatherMap with cities: {cities}")
        except Exception as e:
            logger.error(f"Failed to configure OpenWeatherMap: {e}")

    if "wapi" in data_sources:
        try:
            cities = os.getenv("WAPI_CITIES", "").split(",")
            if not cities or cities == [""]:
                raise ValueError("WAPI_CITIES not configured")
            sources.append(WeatherAPISource(cities))
            logger.info(f"Configured WeatherAPI with cities: {cities}")
        except Exception as e:
            logger.error(f"Failed to configure WeatherAPI: {e}")

    if "file" in data_sources:
        try:
            filepath = os.getenv("CSV_FILE", "weather_data.csv")
            sources.append(CSVSource(filepath))
            logger.info(f"Configured CSV source with file: {filepath}")
        except Exception as e:
            logger.error(f"Failed to configure CSV source: {e}")

    return sources


def ship_to_logzio(logger, records: List[WeatherData]):
    """Batch send records to Logz.io listener."""
    if not records:
        logger.info("No records to ship this cycle.")
        return

    logzio_token = os.getenv("LOGZ_TOKEN")
    logzio_listener = os.getenv("LOGZ_LISTENER", "https://listener.logz.io:8071")

    url = f"{logzio_listener}/?token={logzio_token}"
    headers = {"Content-Type": "application/json"}

    # Convert to newline-delimited JSON
    body = "\n".join(json.dumps(r.to_dict()) for r in records)

    try:
        resp = requests.post(url, headers=headers, data=body, timeout=10)
        resp.raise_for_status()
        logger.info(f"Successfully shipped {len(records)} records to Logz.io")
    except requests.RequestException as e:
        logger.error(f"Failed to ship data to Logz.io: {e}")


def run():
    logger = get_logger()
    sources = load_sources(logger)

    polling_interval = int(os.getenv("POLL_INTERVAL", "60"))

    logger.info("Weather Shipper started.")
    logger.info(f"Polling every {polling_interval} seconds")

    while RUNNING:
        all_records: List[WeatherData] = []

        for source in sources:
            try:
                records = source.fetch()
                all_records.extend(records)
                logger.info(f"Fetched {len(records)} records from {source.__class__.__name__}")
            except FileNotFoundError as e:
                logger.error(f"CSV file not found: {e}")
            except KeyError as e:
                logger.error(f"Missing expected field in source {source.__class__.__name__}: {e}")
            except Exception as e:
                logger.error(f"Unexpected error from {source.__class__.__name__}: {e}")

        # Ship after each cycle
        ship_to_logzio(logger, all_records)

        # Sleep until next cycle
        if RUNNING:
            time.sleep(polling_interval)

    # Final flush before shutdown
    if all_records:
        logger.info("Final flush of records before shutdown...")
        ship_to_logzio(logger, all_records)

    logger.info("Weather Shipper stopped gracefully.")


if __name__ == "__main__":
    # Setup signal handling for Ctrl+C or container stop
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    try:
        run()
    except KeyboardInterrupt:
        sys.exit(0)

