import csv
from pathlib import Path
from typing import List
from models.weather import WeatherData
from sources.base import BaseSource


class CSVSource(BaseSource):
    def __init__(self, filepath: str):
        self.filepath = Path(filepath)

    def fetch(self) -> List[WeatherData]:
        results = []
        with self.filepath.open("r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                results.append(
                    WeatherData(
                        city=row["city"],
                        temperature_celsius=float(row["temperature"]),
                        description=row["description"],
                        source_provider="file",
                    )
                )
        return results
