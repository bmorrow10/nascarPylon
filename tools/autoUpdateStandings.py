#!/usr/bin/env python3
"""
Auto-update standings from NASCAR points feed
Runs after each race to pull latest standings
"""

import csv
import json
from datetime import datetime
from pathlib import Path

import requests

DATA_DIR = Path("data")
STANDINGS_CSV = DATA_DIR / "standings.csv"
STANDINGS_JSON = DATA_DIR / "standings.json"

# NASCAR points feed URL (from ops feed)
POINTS_FEED_URL = "https://cf.nascar.com/cacher/2026/1/points-feed.json"


def fetch_current_standings():
    """Fetch current Cup Series standings from NASCAR"""
    try:
        print("Fetching current standings from NASCAR...")
        response = requests.get(POINTS_FEED_URL, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data
    except Exception as e:
        print(f"❌ Error fetching standings: {e}")
        return None


def parse_standings(data):
    """Parse NASCAR standings data to our format"""
    standings = []

    # NASCAR returns a list directly
    if not isinstance(data, list):
        print("⚠️  Unexpected data format")
        return None

    # Parse each driver
    for driver in data:
        position = driver.get("position")
        car = driver.get("car_no")
        name = driver.get("driver_last_name", driver.get("driver_name", "Unknown"))
        points = driver.get("points", 0)

        if position and car:
            standings.append(
                {
                    "position": int(position),
                    "car": str(car),
                    "driver": name,
                    "points": int(points),
                }
            )

    # Sort by position
    standings.sort(key=lambda x: x["position"])

    # Calculate points back from leader
    if standings:
        leader_points = standings[0]["points"]
        for driver in standings:
            driver["pointsBack"] = leader_points - driver["points"]

    return standings


def save_to_csv(standings):
    """Save standings to CSV"""
    with open(STANDINGS_CSV, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["position", "car", "driver", "pointsBack"])

        for driver in standings:
            writer.writerow(
                [
                    driver["position"],
                    driver["car"],
                    driver["driver"],
                    driver["pointsBack"],
                ]
            )

    print(f"✅ Saved to {STANDINGS_CSV}")


def save_to_json(standings):
    """Save standings to JSON"""
    output = {
        "series": "CUP",
        "season": datetime.now().year,
        "lastUpdated": datetime.now().isoformat(),
        "drivers": standings,
    }

    with open(STANDINGS_JSON, "w") as f:
        json.dump(output, f, indent=2)

    print(f"✅ Saved to {STANDINGS_JSON}")


def main():
    """Main function"""
    print("=" * 60)
    print("NASCAR STANDINGS AUTO-UPDATER")
    print("=" * 60)
    print()

    # Fetch data
    data = fetch_current_standings()
    if not data:
        print("\n❌ Failed to fetch standings")
        print("You can still manually update data/standings.csv")
        return False

    # Parse data
    standings = parse_standings(data)
    if not standings:
        print("\n❌ Failed to parse standings data")
        return False

    print(f"\n📊 Found {len(standings)} drivers")
    print(f"Leader: #{standings[0]['car']} {standings[0]['driver']}")

    # Save
    save_to_csv(standings)
    save_to_json(standings)

    print("\n✅ Standings updated successfully!")
    print(f"   Season: {datetime.now().year}")
    print(f"   Updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")

    return True


if __name__ == "__main__":
    import sys

    success = main()
    sys.exit(0 if success else 1)
