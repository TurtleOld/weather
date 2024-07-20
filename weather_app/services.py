import datetime
import requests
from typing_extensions import Any


def get_lat_lon(city: str) -> tuple[float, float, str]:
    params = {
        "name": city,
        "count": 1,
        "language": "ru",
        "format": "json",
    }

    url = "https://geocoding-api.open-meteo.com/v1/search"

    response = requests.get(url, params=params)

    data = response.json()

    latitude = data["results"][0]["latitude"]
    longitude = data["results"][0]["longitude"]
    tz = data["results"][0]["timezone"]

    return latitude, longitude, tz


def get_list_cities(city: str) -> list[str]:
    params = {
        "name": city,
        "count": 10,
        "language": "ru",
        "format": "json",
    }

    url = "https://geocoding-api.open-meteo.com/v1/search"

    response = requests.get(url, params=params)

    data = response.json()

    cities = []

    for ct in data["results"]:
        cities.append(ct.get("name"))

    return cities


def parse_data(json_data: dict[str, Any]) -> list[dict[str, Any]]:
    current = json_data.get("current", "")
    current_units = json_data.get("current_units", "")
    times = current.get("time", "")
    temperatures = current.get("temperature_2m", "")
    apparent_temperatures = current.get("apparent_temperature", "")
    degree = current_units.get("temperature_2m", "")

    result = [
        {
            "time": datetime.datetime.strptime(times, "%Y-%m-%dT%H:%M"),
            "temperature": temperatures,
            "apparent_temperature": apparent_temperatures,
            "degree": degree,
        }
    ]
    return result


def get_weather_info(city: str):
    lat, lon, tz = get_lat_lon(city)

    params = {
        "name": city,
        "latitude": lat,
        "longitude": lon,
        "current": "temperature_2m,apparent_temperature",
        "timezone": tz,
    }

    url = "https://api.open-meteo.com/v1/forecast"

    response = requests.get(url, params=params)

    data = response.json()

    return parse_data(data)
