#!/usr/bin/env python3
"""
NASCAR Feed API Endpoint Tester
Tests various feed.nascar.com endpoints during a live race
"""

import json
import sys
from urllib.request import urlopen, Request
from datetime import datetime
from pathlib import Path

# Known NASCAR feed endpoints
ENDPOINTS = {
    "live-feed": "https://feed.nascar.com/live-feed.json",
    "flag-state": "https://feed.nascar.com/flag-state.json",
    "lap-times": "https://feed.nascar.com/lap-times.json",
    "loop-data": "https://feed.nascar.com/loop-data.json",
    "pit-stops": "https://feed.nascar.com/pit-stops.json",
    "points": "https://feed.nascar.com/points.json",
}

def test_endpoint(name, url, save_to_file=False):
    """Test a single endpoint and show results"""
    print(f"\n{'='*60}")
    print(f"Testing: {name}")
    print(f"URL: {url}")
    print(f"{'='*60}")
    
    req = Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
    })
    
    try:
        with urlopen(req, timeout=10) as response:
            status = response.status
            content = response.read().decode('utf-8')
            
            print(f"✅ Status: {status}")
            print(f"📦 Size: {len(content)} bytes")
            
            # Try to parse as JSON
            try:
                data = json.loads(content)
                print(f"✅ Valid JSON")
                
                # Show structure
                if isinstance(data, dict):
                    print(f"📊 Top-level keys: {list(data.keys())[:10]}")
                elif isinstance(data, list):
                    print(f"📊 Array with {len(data)} items")
                    if len(data) > 0:
                        print(f"   First item keys: {list(data[0].keys())[:10]}")
                
                # Save to file if requested
                if save_to_file:
                    output_dir = Path("nascar_api_samples")
                    output_dir.mkdir(exist_ok=True)
                    
                    filename = output_dir / f"{name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                    with open(filename, 'w') as f:
                        json.dump(data, f, indent=2)
                    print(f"💾 Saved to: {filename}")
                
                # Show preview
                print(f"\n📋 Preview (first 500 chars):")
                print("-" * 60)
                preview = json.dumps(data, indent=2)[:500]
                print(preview)
                if len(json.dumps(data)) > 500:
                    print("...")
                
                return True, data
                
            except json.JSONDecodeError as e:
                print(f"❌ Invalid JSON: {e}")
                print(f"Content preview: {content[:200]}")
                return False, None
                
    except Exception as e:
        print(f"❌ Error: {e}")
        return False, None


def main():
    """Test all NASCAR feed endpoints"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Test NASCAR feed API endpoints')
    parser.add_argument('--save', action='store_true', 
                       help='Save responses to files')
    parser.add_argument('--endpoint', type=str, 
                       help='Test specific endpoint only')
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("NASCAR FEED API ENDPOINT TESTER")
    print("=" * 60)
    print(f"\n⏰ Test time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\n⚠️  Note: These endpoints only return data during live races!")
    print("   If all fail, the race may not be active yet.\n")
    
    results = {}
    
    if args.endpoint:
        # Test specific endpoint
        if args.endpoint in ENDPOINTS:
            success, data = test_endpoint(args.endpoint, ENDPOINTS[args.endpoint], args.save)
            results[args.endpoint] = success
        else:
            print(f"❌ Unknown endpoint: {args.endpoint}")
            print(f"Available: {', '.join(ENDPOINTS.keys())}")
            return
    else:
        # Test all endpoints
        for name, url in ENDPOINTS.items():
            success, data = test_endpoint(name, url, args.save)
            results[name] = success
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    working = [name for name, success in results.items() if success]
    failing = [name for name, success in results.items() if not success]
    
    if working:
        print(f"\n✅ Working endpoints ({len(working)}):")
        for name in working:
            print(f"   • {name}")
    
    if failing:
        print(f"\n❌ Failed endpoints ({len(failing)}):")
        for name in failing:
            print(f"   • {name}")
    
    if not working:
        print("\n⚠️  No endpoints returned data.")
        print("   This is normal if there's no active race.")
        print("   Try again during Sunday's Clash at Bowman Gray!")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()