# import requests
# import os
# from models.weather import NormalizedWeather
# from datetime import datetime

# API_KEY = os.getenv("WAPI_API_KEY")

# def fetch_weatherapi_data(city: str) -> NormalizedWeather:
#     url = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city}"
#     res = requests.get(url)
#     res.raise_for_status()
#     data = res.json()
#     return NormalizedWeather(
#         location=city,
#         temperature_c=data["current"]["temp_c"],
#         humidity=data["current"]["humidity"],
#         source="weatherapi",
#         timestamp=datetime.strptime(data["location"]["localtime"], "%Y-%m-%d %H:%M"),
#     )


import os
import requests
from typing import List
from models.weather import WeatherData
from sources.base import BaseSource


class WeatherAPISource(BaseSource):
    def __init__(self, cities: List[str]):
        self.api_key = os.getenv("WAPI_API_KEY")
        self.cities = cities

    def fetch(self) -> List[WeatherData]:
        results = []
        for city in self.cities:
            url = f"http://api.weatherapi.com/v1/current.json?key={self.api_key}&q={city}"
            res = requests.get(url)
            res.raise_for_status()
            data = res.json()

            results.append(
                WeatherData(
                    city=city,
                    temperature_celsius=data["current"]["temp_c"],
                    description=data["current"]["condition"]["text"],
                    source_provider="weatherapi",
                )
            )
        return results
