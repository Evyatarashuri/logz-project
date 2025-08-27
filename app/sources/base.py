from abc import ABC, abstractmethod
from typing import List
from models.weather import WeatherData

class BaseSource(ABC):
    @abstractmethod
    def fetch(self) -> List[WeatherData]:
        """Fetch and transform data into unified WeatherData objects."""
        pass
