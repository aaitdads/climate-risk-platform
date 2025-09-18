import os
import json
import argparse
from datetime import datetime
import requests
from dotenv import load_dotenv
import pandas as pd

# Load environment variables
load_dotenv()
API_KEY = os.getenv("METEOSTAT_RAPIDAPI_KEY")

if not API_KEY:
    raise ValueError("❌ Missing API key. Please set METEOSTAT_RAPIDAPI_KEY in your .env file.")

BASE_URL = "https://meteostat.p.rapidapi.com/point"


def fetch_data(lat, lon, start, end, granularity="daily"):
    """
    Fetch Meteostat weather data (daily or hourly).
    For hourly, splits into monthly chunks to avoid 400 errors.
    """
    headers = {
        "x-rapidapi-host": "meteostat.p.rapidapi.com",
        "x-rapidapi-key": API_KEY,
    }

    if granularity == "daily":
        url = f"{BASE_URL}/daily"
        params = {"lat": lat, "lon": lon, "start": start, "end": end}
        r = requests.get(url, headers=headers, params=params, timeout=30)
        r.raise_for_status()
        return r.json()

    elif granularity == "hourly":
        url = f"{BASE_URL}/hourly"
        results = {"data": []}

        # split into monthly chunks
        months = pd.date_range(start=start, end=end, freq="MS")
        for i in range(len(months)):
            chunk_start = months[i].strftime("%Y-%m-%d")
            if i + 1 < len(months):
                chunk_end = (months[i + 1] - pd.Timedelta(days=1)).strftime("%Y-%m-%d")
            else:
                chunk_end = end

            params = {"lat": lat, "lon": lon, "start": chunk_start, "end": chunk_end}
            print(f"📡 Fetching hourly {chunk_start} → {chunk_end} ...")

            r = requests.get(url, headers=headers, params=params, timeout=30)
            r.raise_for_status()
            data = r.json()
            results["data"].extend(data.get("data", []))

        return results

    else:
        raise ValueError("Granularity must be 'daily' or 'hourly'.")


def save_json(data, name, granularity, start, end):
    """
    Save raw Meteostat JSON to data/raw/meteostat with timestamp.
    """
    os.makedirs("data/raw/meteostat", exist_ok=True)
    timestamp = datetime.utcnow().strftime("%Y%m%dT%H%MZ")
    filename = f"data/raw/meteostat/{name}_meteostat_{granularity}_{start}_{end}_{timestamp}.json"

    with open(filename, "w") as f:
        json.dump(data, f, indent=2)

    print(f"✅ Saved {filename}")


def main():
    parser = argparse.ArgumentParser(description="Fetch Meteostat historical weather data")
    parser.add_argument("--lat", type=float, required=True, help="Latitude")
    parser.add_argument("--lon", type=float, required=True, help="Longitude")
    parser.add_argument("--start", type=str, required=True, help="Start date (YYYY-MM-DD)")
    parser.add_argument("--end", type=str, required=True, help="End date (YYYY-MM-DD)")
    parser.add_argument("--name", type=str, default="location", help="Location name for filenames")
    parser.add_argument("--granularity", type=str, choices=["daily", "hourly", "both"], default="daily",
                        help="Data granularity: daily, hourly, or both")

    args = parser.parse_args()

    if args.granularity in ["daily", "both"]:
        daily = fetch_data(args.lat, args.lon, args.start, args.end, "daily")
        save_json(daily, args.name, "daily", args.start, args.end)

    if args.granularity in ["hourly", "both"]:
        hourly = fetch_data(args.lat, args.lon, args.start, args.end, "hourly")
        save_json(hourly, args.name, "hourly", args.start, args.end)


if __name__ == "__main__":
    main()
