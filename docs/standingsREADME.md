# NASCAR Standings Management

## Quick Start

### Option 1: Manual Entry (Recommended for now)

1. **Edit** `data/standings.csv` with current standings
2. **Run**: `python convert_standings.py`
3. **Updated** `data/standings.json` is ready to use

## CSV Format

```csv
position,car,driver,pointsBack
1,5,Larson,0
2,11,Hamlin,3
3,14,Briscoe,15
```

### Column Descriptions

- **position**: Standing position (1-40)
- **car**: Car number (without #)
- **driver**: Driver last name
- **pointsBack**: Points behind leader (0 for leader)

## Files

### CSV File (edit this!)
- `data/standings.csv` - Current points standings

### Generated JSON (don't edit directly!)
- `data/standings.json` - Output file used by pylon

### Scripts
- `convert_standings.py` - Convert CSV to JSON (works offline)
- `scrape_standings.py` - Auto-scraper from ESPN (requires network)

## Future: Auto-Scraping

The `scrape_standings.py` script can fetch live standings from ESPN when network access is available. For now, use the CSV method for offline development.

### To use auto-scraper:
```bash
python scrape_standings.py
```

This will:
1. Fetch current standings from ESPN
2. Match drivers to car numbers
3. Calculate points back from leader
4. Save to `standings.json`

## Data Source

Current standings can be found at:
- https://www.espn.com/racing/standings
- https://www.nascar.com/standings/nascar-cup-series/

## Notes

- All JSON keys use **camelCase** format
- Points shown are "points back" not total points
- Leader always has `pointsBack: 0`
- Update standings.csv manually after each race for now