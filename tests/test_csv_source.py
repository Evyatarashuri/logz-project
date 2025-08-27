import pytest
import tempfile
from app.sources.csv_source import CSVSource
from app.models.weather import WeatherData


def test_csvsource_fetch():
    # Create a temporary CSV file
    csv_content = "city,temperature,description\nBerlin,18.5,Scattered clouds\nSydney,22.1,Sunny\n"

    with tempfile.NamedTemporaryFile(mode="w+", delete=False) as tmp:
        tmp.write(csv_content)
        tmp_path = tmp.name

    source = CSVSource(tmp_path)
    records = source.fetch()

    assert len(records) == 2
    assert records[0].city == "Berlin"
    assert records[0].temperature_celsius == 18.5
    assert records[0].description == "Scattered clouds"
    assert records[0].source_provider == "file"


def test_csvsource_missing_field(tmp_path):
    # CSV without temperature column
    csv_content = "city,description\nBerlin,Clear sky\n"
    file_path = tmp_path / "bad.csv"
    file_path.write_text(csv_content)

    source = CSVSource(str(file_path))

    with pytest.raises(KeyError):
        source.fetch()
