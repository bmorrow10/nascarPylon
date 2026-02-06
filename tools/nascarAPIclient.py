#!/usr/bin/env python3
"""
NASCAR Live Feed API Client
Fetches live race data from NASCAR's cf.nascar.com endpoints

Based on research from:
- Kevinw14/NascarPylon (API structure reference)
- ooohfascinating/NascarApi (endpoint documentation)
"""

import json
from datetime import datetime
from enum import Enum
from pathlib import Path

import requests

DATA_DIR = Path("data")


class Series(Enum):
    """NASCAR Series IDs"""

    CUP = 1
    OREILLY = 2  # O'Reilly Auto Parts Series (formerly Xfinity)
    TRUCKS = 3


class FlagStatus(Enum):
    """Race flag status"""

    NONE = 0
    GREEN = 1
    CAUTION = 2
    RED = 3
    WHITE = 4
    CHECKERED = 5
    ORANGE = 8
    UNKNOWN = 9


class NascarApiClient:
    """Client for accessing NASCAR live feed APIs"""

    def __init__(self):
        self.ops_feed_url = "https://cf.nascar.com/live-ops/live-ops.json"
        # Use the cacher endpoint - has full data including intervals
        self.cacher_feed_url = "https://cf.nascar.com/cacher/live/live-feed.json"
        self.ops_feed = None

    def get_data(self, url, timeout=10):
        """Fetch JSON data from URL"""
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "application/json",
            "Referer": "https://www.nascar.com/",
        }

        try:
            response = requests.get(url, headers=headers, timeout=timeout)
            response.raise_for_status()
            return response.json()
        except requests.HTTPError as e:
            if e.response.status_code == 403:
                print(f"⚠️  Access forbidden (403) - Race may not be active yet")
            else:
                print(f"❌ HTTP Error {e.response.status_code}: {url}")
            return None
        except requests.RequestException as e:
            print(f"❌ Error fetching {url}: {e}")
            return None

    def get_ops_feed(self):
        """
        Get the operations feed which contains URLs for live feeds
        This tells us which races are currently active
        """
        if self.ops_feed is None:
            data = self.get_data(self.ops_feed_url)
            if data:
                self.ops_feed = {
                    "cup": data.get("live_feed_url_series1"),
                    "xfinity": data.get("live_feed_url_series2"),
                    "trucks": data.get("live_feed_url_series3"),
                    "cupPoints": data.get("driver_points_feed_url_series1"),
                    "xfinityPoints": data.get("driver_points_feed_url_series2"),
                    "trucksPoints": data.get("driver_points_feed_url_series3"),
                }
        return self.ops_feed

    def get_live_feed_url(self, series):
        """Get the live feed URL for a specific series"""
        ops = self.get_ops_feed()
        if not ops:
            return None

        if series == Series.CUP:
            return ops.get("cup")
        elif series == Series.OREILLY:
            return ops.get("xfinity")  # API still uses 'xfinity' key
        elif series == Series.TRUCKS:
            return ops.get("trucks")

        return None

    def get_live_feed(self, series=Series.CUP, use_cacher=True):
        """
        Fetch live race feed for specified series
        Returns data in our camelCase format

        Args:
            series: Which series to fetch (CUP, OREILLY, TRUCKS)
            use_cacher: Use cacher endpoint (has intervals) vs basic feed
        """
        if use_cacher:
            # Use cacher endpoint - has full data including delta/intervals
            url = self.cacher_feed_url
        else:
            # Use series-specific endpoint (basic data only)
            url = self.get_live_feed_url(series)
            if not url:
                print(f"⚠️  No live feed URL available for {series.name}")
                return None

        data = self.get_data(url)
        if not data:
            return None

        # Convert to our format
        return self._parse_live_feed(data, series)

    def _parse_live_feed(self, data, series):
        """Parse NASCAR API response to our camelCase format"""

        # Map flag status
        flag_state = data.get("flag_state", 0)
        flag_map = {
            0: "NONE",
            1: "GREEN",
            2: "YELLOW",
            3: "RED",
            4: "WHITE",
            5: "CHECKERED",
            9: "CHECKERED",  # Also checkered
            8: "ORANGE",
        }
        flag_status = flag_map.get(flag_state, "UNKNOWN")

        # Parse vehicles (drivers)
        cars = []
        leader_delta = None

        for idx, vehicle in enumerate(data.get("vehicles", []), 1):
            # Get driver info
            driver_data = vehicle.get("driver", {})
            driver_name = driver_data.get("last_name", "Unknown")

            # Get delta (gap to leader in seconds)
            delta = vehicle.get("delta", None)

            # Leader has delta of 0.0
            if idx == 1 or delta == 0.0:
                leader_delta = 0.0
                interval = None  # Leader has no interval
            else:
                # For non-leaders, delta is the interval to leader
                interval = delta if delta is not None else None

            car = {
                "position": vehicle.get("running_position", idx),
                "car": vehicle.get("vehicle_number", ""),
                "driver": driver_name,
                "interval": interval,
                "lapsCompleted": vehicle.get("laps_completed", 0),
                "passingDifferential": vehicle.get("passing_differential", 0),
                "status": vehicle.get("status", 1),
                "isOnTrack": vehicle.get("is_on_track", True),
                "isOnDVP": vehicle.get("is_on_dvp", False),
                "pitStops": vehicle.get("pit_stops", []),
                # Bonus data from cacher endpoint
                "bestLap": vehicle.get("best_lap", None),
                "bestLapSpeed": vehicle.get("best_lap_speed", None),
                "lastLapSpeed": vehicle.get("last_lap_speed", None),
                "averageSpeed": vehicle.get("average_speed", None),
            }
            cars.append(car)

        # Sort by position to ensure correct order
        cars.sort(key=lambda x: x["position"])

        laps_to_go = data.get("laps_to_go", 0)

        return {
            "series": series.name,
            "track": data.get("track_name", "Unknown"),
            "flag": flag_status,
            "lap": data.get("lap_number", 0),
            "lapsTotal": data.get("laps_in_race", 0),
            "lapsToGo": laps_to_go,
            "lastUpdate": datetime.now().isoformat(),
            "cars": cars,
        }

    def save_live_feed(self, series=Series.CUP, filename="liveRace.json"):
        """Fetch and save live feed to JSON file"""
        data = self.get_live_feed(series)

        if not data:
            print(f"⚠️  No live data available for {series.name}")
            return False

        DATA_DIR.mkdir(exist_ok=True)
        filepath = DATA_DIR / filename

        with open(filepath, "w") as f:
            json.dump(data, f, indent=2)

        print(f"✅ Saved {series.name} live feed to {filepath}")
        print(f"   {data['flag']} - Lap {data['lap']}/{data['lapsTotal']}")
        print(f"   {len(data['cars'])} cars")

        return True


def main():
    """Test the API client"""
    import argparse

    parser = argparse.ArgumentParser(description="Fetch NASCAR live race data")
    parser.add_argument(
        "--series",
        type=str,
        default="CUP",
        choices=["CUP", "OREILLY", "TRUCKS"],
        help="Which series to fetch",
    )
    parser.add_argument(
        "--continuous", action="store_true", help="Poll continuously (every 5 seconds)"
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=5,
        help="Polling interval in seconds (default: 5)",
    )

    args = parser.parse_args()

    # Convert series string to enum
    series = Series[args.series]

    print("=" * 60)
    print("NASCAR LIVE FEED CLIENT")
    print("=" * 60)
    print(f"\n📡 Series: {series.name}")

    client = NascarApiClient()

    if args.continuous:
        print(f"🔄 Polling every {args.interval} seconds (Ctrl+C to stop)\n")
        import time

        try:
            while True:
                client.save_live_feed(series)
                time.sleep(args.interval)
                print()  # Blank line between updates
        except KeyboardInterrupt:
            print("\n\n⏹️  Stopped")
    else:
        print("📥 Fetching once...\n")
        client.save_live_feed(series)


if __name__ == "__main__":
    main()
