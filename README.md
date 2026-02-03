# NASCAR Scoring Pylon 🏁

A real-time LED matrix display system for NASCAR race data. Shows live race positions, championship points standings, and upcoming race schedules across all three NASCAR series.

![Status](https://img.shields.io/badge/status-in%20development-yellow)
![Python](https://img.shields.io/badge/python-3.8+-blue)

## Features

🏎️ **Live Race Display**
- Top 10 positions always visible
- Scrolling field for remaining positions
- Real-time interval gaps to leader/next car
- Battle indicators for cars fighting for position
- Flag status (GREEN/YELLOW/RED) and lap count

📊 **Points Standings**
- Current Cup Series championship standings
- Points deficit to leader
- Easy CSV-based updates

📅 **Schedule View**
- Upcoming races across all three series (Cup, Xfinity, Trucks)
- Countdown to next Cup race
- Playoff race indicators

🤖 **Smart Auto-Detection**
- Automatically switches between LIVE and IDLE modes
- Accounts for rain delays and schedule changes
- Alternates between points and schedule when no race is active

## Quick Start

### 1. Clone & Setup
```bash
git clone https://github.com/yourusername/nascarPylon.git
cd nascarPylon
```

### 2. Test with Mock Data
```bash
# Generate mock race data
python tools/scrapeLiveRace.py --mock

# Run the display
python pylon.py
```

### 3. Update Data

**Schedules:**
```bash
# Edit CSV files in schedules/
vim schedules/cup.csv

# Convert to JSON
python tools/convertSchedules.py
```

**Standings:**
```bash
# Edit standings CSV
vim data/standings.csv

# Convert to JSON
python tools/convertStandings.py
```

## Project Structure

```
nascarPylon/
├── pylon.py                  # Main application
├── data/                     # Race data (JSON files)
├── schedules/                # Race schedules (CSV source files)
├── tools/                    # Data converters & scrapers
├── src/
│   ├── layout.py            # Display layout builders
│   ├── loader.py            # Data loading utilities
│   ├── state.py             # Auto-mode detection logic
│   ├── scheduleUtils.py     # Schedule helper functions
│   └── views/
│       └── cliView.py       # Terminal renderer
└── docs/                     # Documentation
```

## Display Modes

The pylon automatically switches modes:

- **LIVE** - During active races (auto-detected)
- **IDLE** - When no race is active (alternates between points & schedule)

Override automatic detection in `pylon.py`:
```python
MODE_OVERRIDE = "LIVE"  # Force LIVE mode
MODE_OVERRIDE = "IDLE"  # Force IDLE mode
MODE_OVERRIDE = None    # Auto-detect (default)
```

## Getting Live Race Data

### For Sunday's Race

1. **During the race**, capture the HTML structure:
   ```bash
   python tools/inspectNASCAR.py https://www.nascar.com/results/race_center/2026/nascar-cup-series/clash/
   ```

2. **Analyze** `nascar_live.html` to understand the data structure

3. **Update** `tools/scrapeLiveRace.py` with the parsing logic

4. **Run continuously** during race:
   ```bash
   # In a loop or cron job
   python tools/scrapeLiveRace.py
   ```

See [docs/scrappingREADME.md](docs/scrappingREADME.md) for detailed instructions.

## Configuration

### Data Freshness
Edit `src/state.py` to adjust race detection sensitivity:
```python
# Consider data fresh if updated within last 10 minutes
is_race_data_fresh(liveRaceData, maxAgeMinutes=10)

# Race window: 2 hours before to 6 hours after scheduled start
WINDOW_BEFORE = timedelta(hours=2)
WINDOW_AFTER = timedelta(hours=6)
```

### Battle Detection
Edit `src/layout.py` to adjust battle indicator threshold:
```python
BATTLE_THRESHOLD = 0.15  # seconds - cars within this gap show as battling
```

## Roadmap

- [x] CLI display renderer
- [x] Auto-mode detection
- [x] Schedule management (CSV → JSON)
- [x] Points standings
- [ ] Live race data scraper (NASCAR.com)
- [ ] RGB LED matrix support (Raspberry Pi)
- [ ] Stylized car number graphics
- [ ] Visual battle position highlighting
- [ ] Multi-series support (Xfinity, Trucks)
- [ ] Web-based remote display

## Hardware (Planned)

Target setup for LED display:
- RGB LED Matrix panels (64x32 or 128x64)
- Raspberry Pi 4
- [rpi-rgb-led-matrix](https://github.com/hzeller/rpi-rgb-led-matrix) library
- 5V power supply

## Contributing

This is a personal project but feel free to fork and adapt for your own use!

## License

MIT License - See LICENSE file for details

# Acknowledgments

This project was inspired by and builds upon the amazing work of the NASCAR community.

## Inspiration & Prior Art

### 🏆 Direct Inspirations

**u/Leuel48Fan** - [8ft Custom LED NASCAR Scoring Tower](https://www.reddit.com/r/NASCAR/comments/1bsiydv/i_build_an_8ft_custom_led_nascar_scoring_tower/)
- Amazing physical build that inspired this project
- Showed what's possible with LED displays and NASCAR data
- Reddit user who documented their incredible scoring tower

**u/GoDuke4382** (RRoberts4382 on GitHub)
- Created [rNascar23](https://github.com/RRoberts4382/rNascar23-Releases)
- Developed [rNascar23.Sdk](https://github.com/RRoberts4382/rNascar23.Sdk) - C# SDK for NASCAR data
- Pioneered accessing NASCAR's feed.nascar.com endpoints
- Provided invaluable reference for API structure and data sources

## Data Sources

- **NASCAR** - For providing public data feeds at feed.nascar.com
- **ESPN** - For standings and schedule data
- The broader **NASCAR community** on Reddit for discussions and ideas

## Open Source Libraries & Tools

This project wouldn't be possible without:
- Python and the Python community
- Future: [rpi-rgb-led-matrix](https://github.com/hzeller/rpi-rgb-led-matrix) by Henner Zeller

## Community

Special thanks to:
- r/NASCAR subreddit community
- Everyone who shares their projects and inspires others
- Future contributors to this project

---

**If you're inspired by this project, please continue the chain!**

Share your builds, credit your sources, and help the community grow. 🏁

---

**Current Status:** CLI display working, preparing for LED matrix implementation and live data scraping.