import os
import json
import argparse
import pandas as pd


def load_json(filepath):
    """Load a JSON file."""
    with open(filepath, "r") as f:
        return json.load(f)


def flatten_meteostat(data, granularity="daily"):
    """Flatten Meteostat JSON into a DataFrame."""
    df = pd.DataFrame(data.get("data", []))
    if not df.empty:
        df["date"] = pd.to_datetime(df["date"])
    return df


def flatten_openmeteo(data):
    """Flatten Open-Meteo JSON into DataFrames (current + hourly)."""
    dfs = {}

    # Current weather
    current = pd.DataFrame([data["current_weather"]])
    current["time"] = pd.to_datetime(current["time"])
    dfs["current"] = current

    # Hourly forecast
    hourly = pd.DataFrame(data["hourly"])
    if "time" in hourly.columns:
        hourly["time"] = pd.to_datetime(hourly["time"])
    dfs["hourly"] = hourly

    return dfs


def save_dataframe(df, outdir, name):
    """Save DataFrame to CSV in data/processed/."""
    os.makedirs(outdir, exist_ok=True)
    filepath = os.path.join(outdir, f"{name}.csv")
    df.to_csv(filepath, index=False)
    print(f"✅ Saved {filepath}")


def main():
    parser = argparse.ArgumentParser(description="Preprocess raw JSON into clean DataFrames")
    parser.add_argument("--source", type=str, choices=["meteostat", "openmeteo"], required=True,
                        help="Which API source: meteostat or openmeteo")
    parser.add_argument("--file", type=str, required=True, help="Path to raw JSON file")
    parser.add_argument("--granularity", type=str, choices=["daily", "hourly"], default="daily",
                        help="Granularity for Meteostat (ignored for Open-Meteo)")
    parser.add_argument("--name", type=str, default="dataset", help="Name for output CSV")
    args = parser.parse_args()

    data = load_json(args.file)

    if args.source == "meteostat":
        df = flatten_meteostat(data, args.granularity)
        save_dataframe(df, "data/processed/meteostat", args.name)

    elif args.source == "openmeteo":
        dfs = flatten_openmeteo(data)
        for key, df in dfs.items():
            save_dataframe(df, "data/processed/open_meteo", f"{args.name}_{key}")


if __name__ == "__main__":
    main()
