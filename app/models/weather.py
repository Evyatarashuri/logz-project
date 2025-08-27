from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class WeatherData:
    city: str
    temperature_celsius: float
    description: str
    source_provider: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "city": self.city,
            "temperature_celsius": self.temperature_celsius,
            "description": self.description,
            "source_provider": self.source_provider,
        }
