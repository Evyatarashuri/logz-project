import os
import requests
from typing import List
from models.weather import WeatherData
from sources.base import BaseSource


class OpenWeatherMapSource(BaseSource):
    def __init__(self, cities: List[str]):
        self.api_key = os.getenv("OWM_API_KEY")
        self.cities = cities

    def fetch(self) -> List[WeatherData]:
        results = []
        for city in self.cities:
            url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.api_key}&units=metric"
            res = requests.get(url)
            res.raise_for_status()
            data = res.json()

            results.append(
                WeatherData(
                    city=city,
                    temperature_celsius=data["main"]["temp"],
                    description=data["weather"][0]["description"],
                    source_provider="openweathermap",
                )
            )
        return results
