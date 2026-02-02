#!/usr/bin/env python3
"""
NASCAR Live Race Scraper
Fetches live race data from NASCAR.com during active races
"""

import json
import re
from pathlib import Path
from urllib.request import urlopen, Request
from datetime import datetime

DATA_DIR = Path("data")
LIVE_RACE_FILE = DATA_DIR / "liveRace.json"

# NASCAR.com live race URL pattern
NASCAR_LIVE_URL_TEMPLATE = "https://www.nascar.com/results/race_center/{year}/{series}/{race_slug}/"


def parse_mock_data():
    """
    Generate mock live race data for testing with full field
    """
    # Generate a full 30-car field for testing
    cars = [
        {"position": 1, "car": "24", "driver": "Byron", "interval": None},
        {"position": 2, "car": "5", "driver": "Larson", "interval": 0.234},
        {"position": 3, "car": "11", "driver": "Hamlin", "interval": 0.567},
        {"position": 4, "car": "9", "driver": "Elliott", "interval": 0.089},
        {"position": 5, "car": "48", "driver": "Bowman", "interval": 0.145},
        {"position": 6, "car": "12", "driver": "Blaney", "interval": 0.421},
        {"position": 7, "car": "19", "driver": "Truex", "interval": 0.089},
        {"position": 8, "car": "22", "driver": "Logano", "interval": 0.734},
        {"position": 9, "car": "20", "driver": "Bell", "interval": 0.312},
        {"position": 10, "car": "1", "driver": "Chastain", "interval": 0.198},
        # Positions 11+ will scroll
        {"position": 11, "car": "45", "driver": "Reddick", "interval": 0.856},
        {"position": 12, "car": "8", "driver": "Busch", "interval": 1.234},
        {"position": 13, "car": "23", "driver": "Wallace", "interval": 1.567},
        {"position": 14, "car": "99", "driver": "Suarez", "interval": 0.123},
        {"position": 15, "car": "17", "driver": "Buescher", "interval": 2.145},
        {"position": 16, "car": "6", "driver": "Keselowski", "interval": 2.678},
        {"position": 17, "car": "3", "driver": "Dillon", "interval": 3.012},
        {"position": 18, "car": "41", "driver": "Preece", "interval": 0.234},
        {"position": 19, "car": "54", "driver": "Gibbs", "interval": 3.789},
        {"position": 20, "car": "2", "driver": "Cindric", "interval": 4.123},
        {"position": 21, "car": "4", "driver": "Berry", "interval": 4.567},
        {"position": 22, "car": "34", "driver": "McDowell", "interval": 5.234},
        {"position": 23, "car": "77", "driver": "Hocevar", "interval": 0.089},
        {"position": 24, "car": "43", "driver": "Jones", "interval": 6.012},
        {"position": 25, "car": "42", "driver": "Nemechek", "interval": 6.543},
        {"position": 26, "car": "16", "driver": "Allmendinger", "interval": 7.234},
        {"position": 27, "car": "38", "driver": "Gilliland", "interval": 8.012},
        {"position": 28, "car": "51", "driver": "Haley", "interval": 0.145},
        {"position": 29, "car": "15", "driver": "Ware", "interval": 9.456},
        {"position": 30, "car": "10", "driver": "Gragson", "interval": 10.123},
    ]
    
    return {
        "series": "CUP",
        "track": "Bowman Gray",
        "flag": "GREEN",
        "lap": 45,
        "lapsTotal": 200,
        "lastUpdate": datetime.now().isoformat(),
        "cars": cars
    }


def fetch_live_race_data(race_url):
    """
    Fetch live race data from NASCAR.com
    This is a template - needs updating after inspecting HTML during a race
    """
    print(f"🏁 Fetching live race data from NASCAR.com...")
    
    req = Request(race_url, headers={
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
    })
    
    try:
        with urlopen(req) as response:
            html = response.read().decode('utf-8')
            
        # TODO: Parse HTML after inspecting during live race
        print("⚠️  HTML structure needs to be analyzed during an actual race")
        return None
        
    except Exception as e:
        print(f"❌ Error fetching live data: {e}")
        return None


def build_race_url(series="nascar-cup-series", race_slug="clash", year=2026):
    """Build the NASCAR.com race URL"""
    return NASCAR_LIVE_URL_TEMPLATE.format(
        year=year,
        series=series,
        race_slug=race_slug
    )


def scrape_live_race(race_url=None, use_mock=False):
    """
    Main scraper function
    
    Args:
        race_url: NASCAR.com race URL (or None to build from date)
        use_mock: Use mock data for testing (default: False)
    """
    
    if use_mock:
        print("🧪 Using mock race data for testing...")
        data = parse_mock_data()
    else:
        if not race_url:
            race_url = build_race_url()
        
        data = fetch_live_race_data(race_url)
        
        if not data:
            print("⚠️  No live data available, using mock data")
            data = parse_mock_data()
    
    # Save to file
    DATA_DIR.mkdir(exist_ok=True)
    
    with open(LIVE_RACE_FILE, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"✅ Saved live race data to {LIVE_RACE_FILE}")
    
    # Preview
    print(f"\n🏁 {data['flag']} - Lap {data['lap']}/{data['lapsTotal']}")
    print(f"📍 {data['track']} ({data['series']})")
    print(f"📊 {len(data['cars'])} cars in field")
    print(f"\nTop 10:")
    for car in data['cars'][:10]:
        interval = "LEADER" if car['interval'] is None else f"+{car['interval']:.3f}"
        print(f"  {car['position']:>2}. #{car['car']:<3} {car['driver']:<12} {interval}")
    
    return data


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Scrape NASCAR live race data')
    parser.add_argument('--mock', action='store_true', help='Use mock data for testing')
    parser.add_argument('--url', type=str, help='NASCAR.com race URL')
    parser.add_argument('--series', type=str, default='nascar-cup-series', 
                       help='Series slug (nascar-cup-series, xfinity-series, truck-series)')
    parser.add_argument('--race', type=str, default='clash',
                       help='Race slug (e.g., clash, daytona-500)')
    parser.add_argument('--year', type=int, default=2026, help='Year')
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("NASCAR LIVE RACE SCRAPER")
    print("=" * 60)
    
    if args.url:
        race_url = args.url
    else:
        race_url = build_race_url(args.series, args.race, args.year)
    
    print(f"\n🔗 Race URL: {race_url}\n")
    
    scrape_live_race(race_url=race_url, use_mock=args.mock)
    
    print("\n✨ Done!")


if __name__ == "__main__":
    main()