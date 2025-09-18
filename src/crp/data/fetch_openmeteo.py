import os
import json
import argparse
from datetime import datetime
import requests

BASE_URL = "https://api.open-meteo.com/v1/forecast"


def fetch_current_and_forecast(lat, lon, hours=24):
    """
    Fetch current weather + next N hours forecast from Open-Meteo.
    """
    params = {
        "latitude": lat,
        "longitude": lon,
        "current_weather": True,
        "hourly": "temperature_2m,relativehumidity_2m,precipitation",
        "forecast_days": 1 if hours <= 24 else 7,
        "timezone": "auto",
    }

    r = requests.get(BASE_URL, params=params, timeout=30)
    r.raise_for_status()
    return r.json()


def save_json(data, name):
    """
    Save raw Open-Meteo JSON to data/raw/open_meteo with timestamp.
    """
    os.makedirs("data/raw/open_meteo", exist_ok=True)
    timestamp = datetime.utcnow().strftime("%Y%m%dT%H%MZ")
    filename = f"data/raw/open_meteo/{name}_openmeteo_{timestamp}.json"

    with open(filename, "w") as f:
        json.dump(data, f, indent=2)

    print(f"✅ Saved {filename}")


def main():
    parser = argparse.ArgumentParser(description="Fetch live data from Open-Meteo")
    parser.add_argument("--lat", type=float, required=True, help="Latitude")
    parser.add_argument("--lon", type=float, required=True, help="Longitude")
    parser.add_argument("--name", type=str, default="location", help="Location name for filenames")
    parser.add_argument("--hours", type=int, default=24, help="How many hours ahead to fetch")

    args = parser.parse_args()

    data = fetch_current_and_forecast(args.lat, args.lon, args.hours)
    save_json(data, args.name)


if __name__ == "__main__":
    main()
