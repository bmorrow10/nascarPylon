#!/usr/bin/env python3
"""
NASCAR.com HTML Inspector
Use this DURING A LIVE RACE to inspect the HTML structure
and figure out how to extract the data
"""

import sys
from urllib.request import urlopen, Request
from pathlib import Path

def fetch_and_save_html(url, output_file="nascar_live.html"):
    """Fetch NASCAR.com page and save HTML for inspection"""
    
    print(f"🔍 Fetching: {url}")
    
    req = Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
    })
    
    try:
        with urlopen(req) as response:
            html = response.read().decode('utf-8')
        
        # Save to file
        output_path = Path(output_file)
        output_path.write_text(html)
        
        print(f"✅ Saved HTML to: {output_path}")
        print(f"📄 Size: {len(html)} bytes")
        
        # Look for some common patterns
        print("\n🔍 Quick Analysis:")
        
        if "leaderboard" in html.lower():
            print("  ✅ Found 'leaderboard' in HTML")
        
        if "position" in html.lower():
            print("  ✅ Found 'position' in HTML")
            
        if "lap" in html.lower():
            print("  ✅ Found 'lap' in HTML")
            
        if "green" in html.lower() or "yellow" in html.lower():
            print("  ✅ Found flag status indicators")
        
        # Check for JSON data embedded in page
        if '"cars"' in html or '"drivers"' in html:
            print("  ✅ May have JSON data embedded in page!")
            
            # Try to find JSON blocks
            import re
            json_pattern = r'({[^{}]*"(?:cars|drivers|leaderboard)"[^{}]*})'
            matches = re.findall(json_pattern, html)
            if matches:
                print(f"  📊 Found {len(matches)} potential JSON blocks")
        
        print(f"\n💡 Open {output_path} in a text editor to analyze the structure")
        print("   Look for patterns around driver names, positions, intervals")
        
        return html
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


def main():
    """Main entry point"""
    
    if len(sys.argv) < 2:
        print("NASCAR.com HTML Inspector")
        print("\nUsage:")
        print("  python inspectNascar.py <nascar.com_url>")
        print("\nExample for Sunday's Clash:")
        print("  python inspectNascar.py https://www.nascar.com/results/race_center/2026/nascar-cup-series/clash/")
        print("\nRun this DURING the live race to capture the HTML structure!")
        return
    
    url = sys.argv[1]
    fetch_and_save_html(url)


if __name__ == "__main__":
    main()