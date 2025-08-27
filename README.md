# Logz.io Weather Data Shipper

A standalone, production-ready command-line application written in **Python** that polls weather data from multiple sources, normalizes it into a unified JSON schema, and ships it reliably to **Logz.io**.  

Supports:
- **OpenWeatherMap API**
- **WeatherAPI.com API**
- **Local CSV file**

---

## Features
- Modular source architecture (easily add new sources).
- Unified data model for normalized weather logs.
- Configurable via `.env`.
- Reliable shipping to Logz.io (batch + retry handling).
- Graceful shutdown (final flush on exit).
- Unit tests for transformation and CSV parsing.
- Dockerized for portability.

---

## 🗂 Project Structure


logz-project/
┣ app/
┃ ┣ models/ # WeatherData dataclass
┃ ┣ sources/ # OpenWeatherMap, WeatherAPI, CSV source implementations
┃ ┣ logger_config.py # Central logger with Logz.io handler
┃ ┣ main.py # Entry point
┃ ┗ init.py
┣ tests/ # Unit tests (pytest)
┣ Dockerfile
┣ docker-compose.yml
┣ .env
┗ .github/ # GitHub Actions (CI workflow)



---

## ⚙️ Configuration

Create a `.env` file in the root directory:

```env
# API Keys
OWM_API_KEY=your_openweathermap_key
WAPI_API_KEY=your_weatherapi_key

# Logz.io credentials
LOGZ_TOKEN=your_logzio_token
LOGZ_LISTENER=https://listener.logz.io:8071
LOGZ_TYPE=weather
SHIPPER_NAME=multi-source-weather-shipper

# Sources
DATA_SOURCES=owm,wapi,file
OWM_CITIES="berlin,tel aviv"
WAPI_CITIES="sydney,haifa"
CSV_FILE=weather_data.csv

# Polling
POLL_INTERVAL=60   # in seconds


# Photos

![logs](photos/login.png)