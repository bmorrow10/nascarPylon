#!/usr/bin/env python3
"""
NASCAR Standings CSV to JSON Converter
Converts a simple CSV of standings to JSON format
"""

import csv
import json
from pathlib import Path

DATA_DIR = Path("data")
STANDINGS_CSV = DATA_DIR / "standings.csv"
STANDINGS_JSON = DATA_DIR / "standings.json"


def csv_to_standings():
    """Convert standings CSV to JSON"""
    drivers = []
    
    with open(STANDINGS_CSV, 'r') as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            drivers.append({
                "position": int(row["position"]),
                "car": row["car"],
                "driver": row["driver"],
                "pointsBack": int(row["pointsBack"])
            })
    
    return {"drivers": drivers}


def main():
    """Convert standings CSV to JSON"""
    if not STANDINGS_CSV.exists():
        print(f"❌ {STANDINGS_CSV} not found!")
        print("\nCreate a CSV file with columns: position,car,driver,pointsBack")
        return
    
    print("Converting standings from CSV to JSON...")
    
    data = csv_to_standings()
    
    with open(STANDINGS_JSON, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"✅ Saved {len(data['drivers'])} drivers to {STANDINGS_JSON}")
    
    # Preview
    print("\n📊 Top 5:")
    for driver in data['drivers'][:5]:
        back = f"-{driver['pointsBack']}" if driver['pointsBack'] > 0 else "LEADER"
        print(f"  {driver['position']}. #{driver['car']} {driver['driver']} {back}")


if __name__ == "__main__":
    main()