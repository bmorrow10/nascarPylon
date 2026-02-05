# pylon.py

import time
from src.loader import load_json, load_all_schedules
from src.state import determine_state
from src.layout import build_live_layout, build_points_layout, build_schedule_layout
from src.views.cliView import render_live, render_points, render_schedule

SCROLL_DELAY = 2
scroll = 0

# Auto-detect mode based on race data and schedule
# Set to None for auto-detection, or manually set to "LIVE" or "IDLE" to override
MODE_OVERRIDE = None

while True:
    # Determine current mode
    if MODE_OVERRIDE:
        MODE = MODE_OVERRIDE
    else:
        schedules = load_all_schedules()
        try:
            liveData = load_json("liveRace.json")
        except:
            liveData = None
        MODE = determine_state(liveData, schedules)
    
    if MODE == "LIVE":
        data = load_json("liveRace.json")
        layout = build_live_layout(data, scrollOffset=scroll, visibleRows=10)
        render_live(layout)
        scroll += 1
        # Reset scroll when we've shown all positions after P10
        if len(data["cars"]) > 10 and scroll >= len(data["cars"]) - 10:
            scroll = 0
        elif len(data["cars"]) <= 10:
            scroll = 0

    elif MODE == "IDLE":
        # Alternate between points and schedule
        # Show points for 10 seconds, then schedule for 10 seconds
        cycleTime = int(time.time() / 10) % 2
        
        if cycleTime == 0:
            # Show points standings
            data = load_json("standings.json")
            layout = build_points_layout(data)
            render_points(layout)
        else:
            # Show schedule
            layout = build_schedule_layout(load_all_schedules())
            render_schedule(layout)

    time.sleep(SCROLL_DELAY)
    print("\033c", end="")  # clear screen

