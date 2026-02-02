# src/state.py

from datetime import datetime, timedelta
from pathlib import Path
import json

DATA_DIR = Path("data")


def is_race_data_fresh(liveRaceData, maxAgeMinutes=10):
    """
    Check if live race data is recent enough to be considered active
    
    Args:
        liveRaceData: The live race JSON data
        maxAgeMinutes: Maximum age in minutes before data is considered stale
    
    Returns:
        bool: True if data is fresh enough to indicate an active race
    """
    if not liveRaceData:
        return False
    
    # Check if lastUpdate field exists
    lastUpdate = liveRaceData.get("lastUpdate")
    if not lastUpdate:
        # No timestamp, can't determine freshness
        return False
    
    try:
        updateTime = datetime.fromisoformat(lastUpdate)
        now = datetime.now()
        age = now - updateTime
        
        # Consider fresh if updated within the last N minutes
        return age < timedelta(minutes=maxAgeMinutes)
    except:
        return False


def is_race_scheduled_now(schedules):
    """
    Check if a race should be happening right now based on schedule
    
    This accounts for the fact that races might start late due to:
    - Rain delays
    - Pre-race ceremonies
    - TV scheduling
    
    Returns:
        dict or None: Race info if one should be active, None otherwise
    """
    now = datetime.now()
    
    # Check window: 2 hours before scheduled start to 6 hours after
    # (accounts for delays and long races)
    WINDOW_BEFORE = timedelta(hours=2)
    WINDOW_AFTER = timedelta(hours=6)
    
    for sched in schedules:
        for race in sched.get("races", []):
            try:
                raceTime = datetime.fromisoformat(
                    f"{race['date']} {race.get('startTime', '00:00')}"
                )
                
                # Check if we're in the race window
                if (raceTime - WINDOW_BEFORE) <= now <= (raceTime + WINDOW_AFTER):
                    return {
                        "series": sched.get("series"),
                        "race": race,
                        "scheduledTime": raceTime,
                        "inWindow": True
                    }
            except:
                continue
    
    return None


def determine_state(liveRaceData=None, schedules=None):
    """
    Determine what mode the pylon should be in
    
    Priority:
    1. If live race data exists AND is fresh -> LIVE mode
    2. If live race data exists but stale, check schedule -> LIVE if in race window
    3. Otherwise -> IDLE mode (show points + schedule)
    
    Args:
        liveRaceData: Live race JSON data (optional)
        schedules: List of schedule JSON data (optional)
    
    Returns:
        str: "LIVE" or "IDLE"
    """
    
    # Load live race data if not provided
    if liveRaceData is None:
        liveRaceFile = DATA_DIR / "liveRace.json"
        if liveRaceFile.exists():
            try:
                with open(liveRaceFile) as f:
                    liveRaceData = json.load(f)
            except:
                liveRaceData = None
    
    # Check if live data is fresh (updated recently)
    if is_race_data_fresh(liveRaceData, maxAgeMinutes=10):
        print("🏁 LIVE MODE: Fresh race data detected")
        return "LIVE"
    
    # If we have stale data, check if a race should be happening now
    if schedules and liveRaceData:
        scheduledRace = is_race_scheduled_now(schedules)
        if scheduledRace:
            print(f"🏁 LIVE MODE: {scheduledRace['series']} race window active")
            print(f"   (Race might be delayed - last data update was stale)")
            return "LIVE"
    
    # No active race
    print("⏸️  IDLE MODE: No active race detected")
    return "IDLE"


def get_mode_with_detection():
    """
    Convenience function to automatically determine mode
    Loads necessary data and returns the appropriate mode
    """
    from .loader import load_json, load_all_schedules
    
    # Try to load live race data
    try:
        liveData = load_json("liveRace.json")
    except:
        liveData = None
    
    # Load schedules
    try:
        schedules = load_all_schedules()
    except:
        schedules = []
    
    return determine_state(liveData, schedules)
