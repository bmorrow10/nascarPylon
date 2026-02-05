# NASCAR Scoring Pylon 🏁

Real-time LED scoring pylon for NASCAR races. Currently displays live race data in terminal, with LED matrix support coming soon.

**Status:** ✅ Live data working! Successfully tested during 2026 Clash at Bowman Gray

## Features

### ✅ Working Now
- **Live Race Data** - Real-time positions, intervals, and race status
- **Smart Auto-Detection** - Automatically switches between live race and idle modes
- **Position Tracking** - Shows position changes with colored indicators
- **Points Standings** - Championship standings display
- **Schedule Display** - Upcoming races across all three series
- **Color-Coded Display** - Flags, positions, and series all color coded

### 🚧 Coming Soon
- RGB LED matrix display (physical hardware)
- Stylized car number graphics
- Battle position highlighting boxes
- Pit strategy visualization

## Quick Start

### Run the Pylon
```bash
# Auto-detects mode (LIVE during races, IDLE otherwise)
python pylon.py
```

### Pull Live Race Data
```bash
# Continuous polling during race (every 5 seconds)
python tools/nascarAPIclient.py --series CUP --continuous
```

### Update Schedules & Standings
```bash
# After editing CSV files in schedules/ or data/
python tools/convertSchedules.py
python tools/convertStandings.py
```

## Project Structure

```
nascarPylon/
├── pylon.py              # Main application
├── data/                 # Race data & JSON files
├── schedules/            # Race schedules (edit CSVs here)
├── src/                  # Core Python modules
│   ├── layout.py         # Display layouts
│   ├── state.py          # Auto-mode detection
│   └── views/cliView.py  # Terminal renderer
├── tools/                # Utilities & scrapers
└── docs/                 # Documentation
```

## Display Modes

**LIVE MODE** (during active races):
- Top 10 positions always visible
- Scrolling field for 11+
- Real-time intervals to leader
- Position change indicators (↑↓)
- Flag status, lap count, laps to go

**IDLE MODE** (no active race):
- Alternates between points standings and schedule
- Shows next race countdown
- Playoff race indicators

## Data Management

All data is managed through simple CSV files:

**Schedules:** `schedules/cup.csv`, `schedules/oreilly.csv`, `schedules/trucks.csv`  
**Standings:** `data/standings.csv`

After editing CSVs, run the converters to update JSON files.

## NASCAR API

Live data comes from NASCAR's public endpoints:
- Operations Feed: `cf.nascar.com/live-ops/live-ops.json`
- Live Race Feed: `cf.nascar.com/cacher/live/live-feed.json`

See `docs/nascarapiREADME.md` for full API documentation.

## Requirements

```bash
pip install requests
```

## Acknowledgments

Inspired by and built upon the work of:
- **u/Leuel48Fan** - [8ft LED NASCAR Scoring Tower](https://www.reddit.com/r/NASCAR/comments/1bsiydv/)
- **u/GoDuke4382** (RRoberts4382) - [rNascar23.Sdk](https://github.com/RRoberts4382/rNascar23.Sdk)
- **Kevinw14** - [NascarPylon](https://github.com/Kevinw14/NascarPylon)
- **ooohfascinating** - [NascarApi Documentation](https://github.com/ooohfascinating/NascarApi)

## Contributing

Issues and pull requests welcome! See the issues tab for planned features and known bugs.

## License

MIT License - See LICENSE file

---

**Live Data Successfully Tested:** 2026 Cook Out Clash at Bowman Gray Stadium 🏁
