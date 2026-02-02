#!/usr/bin/env python3
"""
CSV to JSON Schedule Converter
Converts NASCAR schedule CSVs to JSON with camelCase keys
"""

import csv
import json
from pathlib import Path

# Define the mapping and series info
SERIES_CONFIG = {
    "cup.csv": {"series": "CUP", "output": "sched.json"},
    "oreilly.csv": {"series": "XFINITY", "output": "schedOR.json"},
    "trucks.csv": {"series": "TRUCKS", "output": "schedTruck.json"}
}

SCHEDULES_DIR = Path("schedules")
DATA_DIR = Path("data")


def csv_to_json(csv_path, series_name):
    """Convert a CSV schedule to JSON format with camelCase keys"""
    races = []
    
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            race = {
                "round": int(row["round"]),
                "raceName": row["raceName"],
                "track": row["track"],
                "location": row["location"],
                "date": row["date"],
                "day": row["day"],
                "startTime": row["startTime"],
                "broadcast": row["broadcast"],
                "distance": row["distance"],
                "laps": int(row["laps"]),
                "isChase": row["isChase"].lower() == "true"
            }
            races.append(race)
    
    return {
        "series": series_name,
        "timezone": "ET",
        "races": races
    }


def main():
    """Convert all CSV schedules to JSON"""
    # Create data directory if it doesn't exist
    DATA_DIR.mkdir(exist_ok=True)
    
    print("Converting NASCAR schedules from CSV to JSON...\n")
    
    for csv_file, config in SERIES_CONFIG.items():
        csv_path = SCHEDULES_DIR / csv_file
        
        if not csv_path.exists():
            print(f"⚠️  Warning: {csv_file} not found, skipping...")
            continue
        
        # Convert CSV to JSON
        data = csv_to_json(csv_path, config["series"])
        
        # Write JSON file
        output_path = DATA_DIR / config["output"]
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ {csv_file} → {config['output']} ({len(data['races'])} races)")
    
    print("\n✨ Conversion complete!")


if __name__ == "__main__":
    main()