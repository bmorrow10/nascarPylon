# NASCAR Pylon

Real-time scoring display for NASCAR races. Shows live positions, intervals, points standings, and race schedules. Built for LED matrix displays with development tools included.

**Status:** Live data tested and working (2026 Clash at Bowman Gray Stadium)

## Features

### Live Race Display
- Real-time positions with intervals to leader
- Automatic scrolling for full field (30+ cars)
- Position change tracking
- Battle indicators for cars within 0.15 seconds
- Flag status, lap count, and laps remaining
- Pit stop detection and status indicators

### Points Standings
- Championship standings for Cup Series
- Points deficit to leader
- Easy CSV-based updates

### Schedule Display
- Upcoming races across all three series
- Countdown to next race
- Playoff race indicators

### Automation
- Auto-detects race start/end
- Switches between LIVE and IDLE modes
- Background poller runs continuously
- Handles rain delays and schedule changes

## Quick Start

```bash
# Clone repository
git clone https://github.com/bmorrow10/nascarPylon.git
cd nascarPylon

# Install dependencies
pip install -r requirements.txt

# Start background poller
./poller.sh start

# Run display (choose one):
python pylon.py           # Terminal display
python webDisplay.py      # Web browser display
```

## Display Options

### Terminal Display
Text-based display with color coding and auto-mode detection.

```bash
python pylon.py
```

### Web Display
Modern web interface accessible from any device.

```bash
python webDisplay.py
# Open http://localhost:5000 in browser
```

### LED Matrix (Hardware)
For physical LED panels (coming soon).

## Project Structure

```
nascarPylon/
├── pylon.py                    # Terminal display
├── webDisplay.py               # Web interface
├── data/                       # Race data (JSON)
├── schedules/                  # CSV schedule files
├── tools/
│   ├── live_poller.py         # Background data collector
│   ├── nascarAPIclient.py     # NASCAR API client
│   ├── convertSchedules.py    # CSV to JSON converter
│   └── convertStandings.py    # Standings converter
├── src/
│   ├── layout.py              # Display layout builders
│   ├── loader.py              # Data loading
│   ├── state.py               # Auto-mode detection
│   └── views/cliView.py       # Terminal renderer
├── templates/
│   └── pylon.html             # Web display template
└── docs/                      # Documentation
```

## Data Management

### Schedules
Edit CSV files in `schedules/` directory:
- `cup.csv` - Cup Series
- `oreilly.csv` - O'Reilly Auto Parts Series
- `trucks.csv` - Craftsman Truck Series

After editing, convert to JSON:
```bash
python tools/convertSchedules.py
```

### Standings
Edit `data/standings.csv`, then convert:
```bash
python tools/convertStandings.py
```

## Background Poller

The poller automatically fetches live race data:

```bash
# Start poller
./poller.sh start

# Check status
./poller.sh status

# View logs
./poller.sh logs

# Stop poller
./poller.sh stop
```

Install as system service (auto-start on boot):
```bash
./poller.sh install
```

## API

Live data comes from NASCAR's public endpoints:
- Operations Feed: `cf.nascar.com/live-ops/live-ops.json`
- Race Data: `cf.nascar.com/cacher/live/live-feed.json`

The poller checks for active races every 30 seconds and polls every 5 seconds during races.

## Auto-Mode Detection

The display automatically switches modes:

**LIVE MODE** - During active races (auto-detected via)
- Fresh data (updated within 10 minutes)
- Race window (2 hours before to 6 hours after scheduled start)

**IDLE MODE** - When no race is active
- Alternates between points standings and schedule
- 10 seconds on each view

## Configuration

### Race Detection
Edit `src/state.py`:
```python
POLL_INTERVAL_RACE = 5      # Seconds between polls during race
POLL_INTERVAL_IDLE = 30     # Seconds between schedule checks
```

### Battle Detection
Edit `src/layout.py`:
```python
BATTLE_THRESHOLD = 0.15  # Seconds - cars within this gap
```

## Requirements

- Python 3.8 or higher
- `requests` - API calls
- `flask` - Web display

Install all dependencies:
```bash
pip install -r requirements.txt
```

## Hardware (Planned)

Target setup for physical LED display:
- RGB LED Matrix panels (128x64 recommended)
- Raspberry Pi 4 (4GB or 8GB)
- Adafruit RGB Matrix HAT
- 5V power supply (high amperage)

Software:
- [rpi-rgb-led-matrix](https://github.com/hzeller/rpi-rgb-led-matrix) library

## Roadmap

- [x] Live race data integration
- [x] Auto-mode detection
- [x] Background poller service
- [x] Web-based display
- [x] Terminal display with colors
- [x] Position change tracking
- [ ] Physical LED matrix support
- [ ] Stylized car number graphics
- [ ] Battle position highlighting boxes
- [ ] Pit strategy visualization
- [ ] Multi-series auto-detection

## Acknowledgments

This project was inspired by:
- **u/Leuel48Fan** - [8ft LED NASCAR Scoring Tower](https://www.reddit.com/r/NASCAR/comments/1bsiydv/)
- **u/GoDuke4382** (RRoberts4382) - [rNascar23.Sdk](https://github.com/RRoberts4382/rNascar23.Sdk)
- **Kevinw14** - [NascarPylon](https://github.com/Kevinw14/NascarPylon)
- **ooohfascinating** - [NascarApi](https://github.com/ooohfascinating/NascarApi)

## License

MIT License - See LICENSE file for details.

## Contributing

Issues and pull requests welcome. This is a hobby project built by a NASCAR fan for NASCAR fans.
