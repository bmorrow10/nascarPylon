#!/usr/bin/env python3
"""
NASCAR Cup Series Standings Scraper
Scrapes current standings from ESPN and saves to JSON with camelCase keys
"""

import json
import re
from pathlib import Path
from urllib.request import urlopen, Request
from html.parser import HTMLParser

DATA_DIR = Path("data")
STANDINGS_FILE = DATA_DIR / "standings.json"

ESPN_CUP_URL = "https://www.espn.com/racing/standings"


class StandingsParser(HTMLParser):
    """Parse ESPN standings table"""
    
    def __init__(self):
        super().__init__()
        self.in_table = False
        self.in_row = False
        self.current_row = []
        self.drivers = []
        self.col_index = 0
        
    def handle_starttag(self, tag, attrs):
        # Look for table rows
        if tag == "tr":
            self.in_row = True
            self.current_row = []
            self.col_index = 0
            
    def handle_endtag(self, tag):
        if tag == "tr" and self.in_row:
            self.in_row = False
            # Process completed row if it has data
            if len(self.current_row) >= 7:
                try:
                    # Extract: rank, driver name, points, wins, poles, top5, top10
                    rank = int(self.current_row[0])
                    driver_full = self.current_row[1]
                    points = int(self.current_row[2])
                    
                    # Extract last name from driver (simple approach)
                    driver = driver_full.split()[-1] if driver_full else "Unknown"
                    
                    # For now, we'll extract car number later
                    # This will need enhancement to get actual car numbers
                    self.drivers.append({
                        "position": rank,
                        "driver": driver,
                        "points": points,
                        "pointsBack": 0  # Will calculate later
                    })
                except (ValueError, IndexError):
                    pass
                    
    def handle_data(self, data):
        if self.in_row:
            data = data.strip()
            if data:
                self.current_row.append(data)


def fetch_standings():
    """Fetch and parse standings from ESPN"""
    print("🏁 Fetching standings from ESPN...")
    
    # Create request with headers to avoid blocking
    req = Request(ESPN_CUP_URL, headers={
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
    })
    
    try:
        with urlopen(req) as response:
            html = response.read().decode('utf-8')
            
        parser = StandingsParser()
        parser.feed(html)
        
        if not parser.drivers:
            print("⚠️  No standings data found")
            return None
            
        # Calculate points back from leader
        leader_points = parser.drivers[0]["points"]
        for driver in parser.drivers:
            driver["pointsBack"] = leader_points - driver["points"]
        
        print(f"✅ Found {len(parser.drivers)} drivers")
        return parser.drivers
        
    except Exception as e:
        print(f"❌ Error fetching standings: {e}")
        return None


def get_car_number_mapping():
    """
    Manual mapping of driver last names to car numbers
    This should be updated periodically or scraped from another source
    """
    return {
        "Larson": "5",
        "Hamlin": "11", 
        "Briscoe": "14",
        "Byron": "24",
        "Bell": "20",
        "Blaney": "12",
        "Logano": "22",
        "Elliott": "9",
        "Reddick": "45",
        "Chastain": "1",
        "Wallace": "23",
        "van Gisbergen": "88",
        "Bowman": "48",
        "Cindric": "2",
        "Dillon": "3",
        "Berry": "4",
        "Buescher": "17",
        "Preece": "41",
        "Gibbs": "54",
        "Keselowski": "6",
        "Busch": "8",
        "McDowell": "34",
        "Hocevar": "77",
        "Jones": "43",
        "Nemechek": "42",
        "Allmendinger": "16",
        "Gilliland": "38",
        "Smith": "71",
        "Suarez": "99",
        "Stenhouse": "47",
        "Haley": "51",
        "Custer": "41",
        "Ty Dillon": "10",
        "Gragson": "10",
        "Herbst": "98",
        "Ware": "15",
        "Legge": "50",
        "Johnson": "84",
    }


def add_car_numbers(drivers):
    """Add car numbers to driver standings"""
    car_mapping = get_car_number_mapping()
    
    for driver in drivers:
        driver_name = driver["driver"]
        # Try to find car number
        if driver_name in car_mapping:
            driver["car"] = car_mapping[driver_name]
        else:
            # Default to position if not found
            driver["car"] = f"#{driver['position']}"
            print(f"⚠️  No car number found for {driver_name}, using placeholder")
    
    return drivers


def save_standings(drivers, limit=None):
    """Save standings to JSON file"""
    if limit:
        drivers = drivers[:limit]
    
    output = {"drivers": drivers}
    
    DATA_DIR.mkdir(exist_ok=True)
    
    with open(STANDINGS_FILE, 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"✅ Saved {len(drivers)} drivers to {STANDINGS_FILE}")


def main():
    """Main scraper function"""
    print("=" * 50)
    print("NASCAR CUP SERIES STANDINGS SCRAPER")
    print("=" * 50)
    
    # Fetch standings from ESPN
    drivers = fetch_standings()
    
    if not drivers:
        print("\n❌ Failed to fetch standings")
        return
    
    # Add car numbers
    drivers = add_car_numbers(drivers)
    
    # Save full standings
    save_standings(drivers)
    
    # Show preview
    print("\n📊 Top 10 Preview:")
    print("-" * 50)
    for i, driver in enumerate(drivers[:10], 1):
        back = f"-{driver['pointsBack']}" if driver['pointsBack'] > 0 else "LEADER"
        print(f"{i:2}  #{driver['car']:<3}  {driver['driver']:<20}  {back:>8}")
    
    print("\n✨ Scraping complete!")


if __name__ == "__main__":
    main()