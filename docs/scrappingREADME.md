# NASCAR Live Race Scraping - Workflow for Sunday

## Game Plan for the Clash at Bowman Gray (Sunday, Feb 1)

### Before the Race

1. **Find the NASCAR.com race URL**
   - Go to https://www.nascar.com/
   - Navigate to the Clash race page
   - The URL should be something like:
     `https://www.nascar.com/results/race_center/2026/nascar-cup-series/clash/`

### During the Race (IMPORTANT!)

2. **Capture the HTML structure** (Do this while the race is LIVE)
   ```bash
   python inspectNascar.py https://www.nascar.com/results/race_center/2026/nascar-cup-series/clash/
   ```
   
   This will:
   - Download the live HTML
   - Save it to `nascar_live.html`
   - Look for JSON data patterns
   - Give you clues about the structure

3. **Analyze the HTML file**
   - Open `nascar_live.html` in a text editor
   - Search for driver names you know (like "Byron", "Larson")
   - Look for position numbers
   - Find interval/gap times
   - Identify the flag status (GREEN/YELLOW/RED)
   - Look for lap count

4. **Update the scraper**
   - Once you understand the HTML structure, update `scrapeLiveRace.py`
   - Modify the `LiveRaceParser` class to extract the data
   - Test it during the race!

### For Testing Now (Before Sunday)

Use **mock mode** to test the display:

```bash
# Generate mock race data
python tools/scrapeLiveRace.py --mock

# This creates data/liveRace.json with fake data
# Then run pylon.py with MODE = "LIVE" to see it work
```

## Why We Need to Wait for a Live Race

NASCAR.com's live leaderboard is **dynamic** - it's loaded with JavaScript during races. We need to:
1. See the actual HTML structure during a live race
2. Find where the position/interval data is embedded
3. Determine if it's in JSON format or HTML tables

## Alternative: Manual Data Entry During Race

If scraping proves difficult, we can create a simple **manual entry tool**:
- You watch the race on TV
- Type in top 10 positions + intervals
- Script updates the JSON file
- Pylon displays it

This is less cool but 100% reliable!

## Files

- `tools/scrapeLiveRace.py` - The main scraper (needs updating after inspecting)
- `inspectNascar.py` - Helper to capture HTML during live race
- `data/liveRace.json` - Output file (pylon reads this)

## Next Steps After We Have Live Data Working

1. **Auto-mode detection** - Check if there's a live race happening
2. **Combined display** - Show points + schedule when no race is active
3. **Continuous scraping** - Poll NASCAR.com every 5-10 seconds during races