# pylon.py

import time

from src.layout import build_live_layout, build_points_layout, build_schedule_layout
from src.loader import load_all_schedules, load_json
from src.state import determine_state
from src.views.cliView import (
    clear_position_history,
    render_live,
    render_points,
    render_schedule,
)

SCROLL_DELAY = 2  # Seconds between screen updates
scroll = 0
last_mode = None

print("=" * 60)
print("NASCAR SCORING PYLON")
print("=" * 60)
print("🔍 Auto-detecting race status...")
print("Press Ctrl+C to stop\n")

while True:
    try:
        # Load schedules
        schedules = load_all_schedules()

        # Try to load live race data
        try:
            liveData = load_json("liveRace.json")
        except:
            liveData = None

        # Auto-detect current mode
        MODE = determine_state(liveData, schedules)

        # Clear position history when switching modes
        if MODE != last_mode:
            clear_position_history()
            if last_mode is not None:  # Don't print on startup
                print(f"\n{'=' * 60}")
                print(f"🔄 Mode changed: {last_mode} → {MODE}")
                print(f"{'=' * 60}\n")
            last_mode = MODE

        # ===== LIVE MODE =====
        if MODE == "LIVE":
            if not liveData:
                print("⚠️  LIVE mode detected but no data file available")
                print("   Waiting for live race data...")
                time.sleep(5)
                continue

            layout = build_live_layout(liveData, scrollOffset=scroll, visibleRows=10)
            render_live(layout)

            # Handle scrolling for positions 11+
            total_cars = len(liveData.get("cars", []))
            if total_cars > 10:
                scroll += 1
                if scroll >= total_cars - 10:
                    scroll = 0
            else:
                scroll = 0

        # ===== IDLE MODE =====
        elif MODE == "IDLE":
            # Alternate between points and schedule every 10 seconds
            cycle_time = int(time.time() / 10) % 2

            if cycle_time == 0:
                # Show points standings
                try:
                    data = load_json("standings.json")
                    layout = build_points_layout(data)
                    render_points(layout)
                except Exception as e:
                    print(f"⚠️  Error loading standings: {e}")
                    print("   Check that data/standings.json exists")
            else:
                # Show schedule
                try:
                    layout = build_schedule_layout(schedules)
                    render_schedule(layout)
                except Exception as e:
                    print(f"⚠️  Error loading schedule: {e}")

        # Update display
        time.sleep(SCROLL_DELAY)
        print("\033c", end="")  # Clear screen

    except KeyboardInterrupt:
        print("\n\n" + "=" * 60)
        print("🏁 Shutting down NASCAR Pylon...")
        print("=" * 60)
        break

    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        print("   Retrying in 5 seconds...")
        time.sleep(5)
