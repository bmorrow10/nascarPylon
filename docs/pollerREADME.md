# NASCAR Live Data Poller

Automated background service that polls NASCAR's API during races and keeps `data/liveRace.json` updated.

## Features

✅ **Fully Automatic**
- Checks race schedule every 30 seconds
- Starts polling when race window opens (2 hours before to 6 hours after)
- Polls every 5 seconds during active races
- Stops polling when race window closes

✅ **Smart Error Handling**
- Retries on network errors
- Stops after 10 consecutive failures (prevents hammering API)
- Logs all activity for debugging

✅ **Multi-Series Support**
- Automatically detects which series is racing (Cup, O'Reilly, Trucks)
- Switches series as needed

✅ **Logging**
- All activity logged to `logs/poller.log`
- Errors logged to `logs/poller-error.log`
- Timestamps on everything

## Quick Start

### Manual Mode (Testing)

```bash
# Start poller (runs in foreground)
python3 tools/livePoller.py

# Or run in background
python3 tools/livePoller.py &

# View logs
tail -f logs/poller.log
```

### Easy Management Script

```bash
# Make script executable
chmod +x poller.sh

# Start poller in background
./poller.sh start

# Check status
./poller.sh status

# View live logs
./poller.sh logs

# Stop poller
./poller.sh stop
```

### Install as System Service (Recommended)

This makes the poller start automatically on boot and restart if it crashes:

```bash
# Install service
./poller.sh install

# Check status
sudo systemctl status nascar-poller

# View logs
journalctl -u nascar-poller -f

# Stop service
sudo systemctl stop nascar-poller

# Start service
sudo systemctl start nascar-poller

# Uninstall
./poller.sh uninstall
```

## How It Works

### Race Detection
1. Loads all three series schedules
2. Checks if current time is within race window
3. Race window = 2 hours before scheduled start to 6 hours after
4. Accounts for rain delays, pre-race shows, etc.

### Polling Logic
```
Every 30 seconds:
  ├─ Check if race window is active
  │
  ├─ If YES and not currently polling:
  │   └─ Start polling every 5 seconds
  │
  ├─ If NO and currently polling:
  │   └─ Stop polling
  │
  └─ If currently polling:
      ├─ Fetch live data from NASCAR API
      ├─ Save to data/liveRace.json
      ├─ Log success/failure
      └─ If 10 errors in a row → stop polling
```

### Data Flow
```
NASCAR API (cf.nascar.com/cacher/live/live-feed.json)
    ↓
Live Poller (tools/livePoller.py)
    ↓
data/liveRace.json
    ↓
Pylon Display (pylon.py)
```

## Configuration

Edit `tools/livePoller.py` to adjust:

```python
POLL_INTERVAL_RACE = 5      # Seconds between polls during race
POLL_INTERVAL_IDLE = 30     # Seconds between schedule checks
MAX_CONSECUTIVE_ERRORS = 10 # Stop after this many errors
```

## Logs

**poller.log** - Normal activity
```
2026-02-04 20:00:15 - INFO - ⏸️  No race active - checking schedule...
2026-02-04 20:02:30 - INFO - 🏁 Starting live polling for CUP
2026-02-04 20:02:30 - INFO -    Race: Cook Out Clash at Bowman Gray
2026-02-04 20:02:35 - INFO - ✅ CUP: Lap 1/200 - GREEN - 23 cars
2026-02-04 20:02:40 - INFO - ✅ CUP: Lap 2/200 - GREEN - 23 cars
```

**poller-error.log** - Errors only
```
2026-02-04 20:15:23 - ERROR - ❌ Error polling data: HTTPError 503
2026-02-04 20:15:28 - WARNING - ⚠️  API returned no data
```

## Troubleshooting

### Poller won't start
```bash
# Check if already running
./poller.sh status

# Check logs for errors
tail -50 logs/poller.log
```

### No data being saved
```bash
# Check if race window is active
python3 -c "from src.loader import load_all_schedules; from src.state import is_race_scheduled_now; print(is_race_scheduled_now(load_all_schedules()))"

# Manually test API
python3 tools/nascarAPIclient.py --series CUP
```

### Service won't auto-start on boot
```bash
# Check service status
sudo systemctl status nascar-poller

# Check if enabled
sudo systemctl is-enabled nascar-poller

# Re-enable
sudo systemctl enable nascar-poller
```

## Next Steps

1. **Test during next race** - Make sure it starts/stops automatically
2. **Monitor logs** - Watch for any errors or issues
3. **Adjust intervals** - Tune polling rate if needed
4. **Set up notifications** - Get alerts when poller starts/stops (optional)

---

**Status:** Ready for production use! Tested during 2026 Clash at Bowman Gray.
