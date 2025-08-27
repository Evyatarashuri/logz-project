from abc import ABC, abstractmethod
from typing import List
from models.weather import WeatherData

class BaseSource(ABC):
    @abstractmethod
    def fetch(self) -> List[WeatherData]:
        """Fetch and transform data into unified WeatherData objects."""
        pass

# This file defines an abstract base class for weather data sources, enforcing a unified interface.
# Any subclass must implement the fetch method to return a list of WeatherData objects.