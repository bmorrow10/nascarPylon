#!/usr/bin/env python3
"""
NASCAR Pylon Web Display
Flask-based web interface for headless servers

Access from any device with a browser:
http://your-server-ip:5000
"""

import json
import sys
from datetime import datetime
from pathlib import Path

from flask import Flask, jsonify, render_template

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent))

from src.layout import build_live_layout, build_points_layout, build_schedule_layout
from src.loader import load_all_schedules, load_json
from src.state import determine_state

app = Flask(__name__)

# Global state
current_mode = "IDLE"
scroll_offset = 0


@app.route("/")
def index():
    """Main display page"""
    return render_template("pylon.html")


@app.route("/api/data")
def get_data():
    """API endpoint that returns current pylon data"""
    global current_mode, scroll_offset

    # Load schedules
    schedules = load_all_schedules()

    # Try to load live data
    try:
        live_data = load_json("liveRace.json")
    except:
        live_data = None

    # Determine mode
    current_mode = determine_state(live_data, schedules)

    response = {"mode": current_mode, "timestamp": datetime.now().isoformat()}

    # Build layout based on mode
    if current_mode == "LIVE" and live_data:
        layout = build_live_layout(
            live_data, scrollOffset=scroll_offset, visibleRows=10
        )
        response["data"] = layout

        # Update scroll
        total_cars = len(live_data.get("cars", []))
        if total_cars > 10:
            scroll_offset = (scroll_offset + 1) % (total_cars - 10)
        else:
            scroll_offset = 0

    elif current_mode == "IDLE":
        # Alternate between points and schedule
        import time

        cycle_time = int(time.time() / 10) % 2

        if cycle_time == 0:
            try:
                data = load_json("standings.json")
                layout = build_points_layout(data)
                response["data"] = layout
            except:
                response["data"] = None
        else:
            try:
                layout = build_schedule_layout(schedules)
                response["data"] = layout
            except:
                response["data"] = None

    return jsonify(response)


@app.route("/api/status")
def get_status():
    """System status endpoint"""
    try:
        live_data = load_json("liveRace.json")
        last_update = live_data.get("lastUpdate", "Unknown")
    except:
        last_update = "No data"

    return jsonify(
        {"mode": current_mode, "lastUpdate": last_update, "server": "running"}
    )


if __name__ == "__main__":
    print("=" * 60)
    print("NASCAR PYLON WEB DISPLAY")
    print("=" * 60)
    print("\nStarting web server...")
    print("Access from any device at:")
    print("  http://localhost:5000")
    print("  http://<your-server-ip>:5000")
    print("\nPress Ctrl+C to stop\n")

    # Run on all interfaces so you can access remotely
    app.run(host="0.0.0.0", port=5000, debug=False)
