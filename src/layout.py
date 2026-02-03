# src/layout.py

from datetime import datetime
from .scheduleUtils import countdown_to

BATTLE_THRESHOLD = 0.15  # seconds


# =========================
# LIVE RACE LAYOUT
# =========================

def annotate_battles(cars):
    for car in cars:
        car["battling"] = (
            car.get("interval") is not None
            and car["interval"] < BATTLE_THRESHOLD
        )
    return cars


def build_live_layout(data, scrollOffset=0, visibleRows=10):
    cars = annotate_battles(data["cars"])

    topFixed = cars[:10]
    scrolling = cars[10 + scrollOffset : 10 + scrollOffset + visibleRows]

    return {
        "mode": "LIVE",
        "header": {
            "flag": data["flag"],
            "lap": data["lap"],
            "total": data["lapsTotal"],
            "lapsToGo": data.get("lapsToGo", 0)
        },
        "fixed": topFixed,
        "scrolling": scrolling
    }


# =========================
# CUP POINTS STANDINGS
# =========================

def build_points_layout(data):
    return {
        "mode": "POINTS",
        "header": {
            "title": "NASCAR CUP SERIES POINT STANDINGS"
        },
        "drivers": data["drivers"]
    }


# =========================
# SCHEDULE + NEXT CUP RACE
# =========================

def build_schedule_layout(allSchedules):
    now = datetime.now()
    rows = []
    nextCupRace = None

    for sched in allSchedules:
        series = sched.get("series", "UNKNOWN")

        for race in sched.get("races", []):
            raceDt = datetime.fromisoformat(
                f"{race['date']} {race.get('startTime', '00:00')}"
            )

            if raceDt >= now:
                rows.append({
                    "date": race["date"],
                    "time": race.get("startTime", ""),
                    "name": race.get("raceName", "UNKNOWN"),
                    "track": race.get("track", ""),
                    "location": race.get("location", ""),
                    "broadcast": race.get("broadcast", ""),
                    "laps": race.get("laps", ""),
                    "distance": race.get("distance", ""),
                    "series": series,
                    "isChase": race.get("isChase", False)
                })

                if series == "CUP" and nextCupRace is None:
                    nextCupRace = race

    rows.sort(key=lambda r: (r["date"], r["time"]))

    header = "UPCOMING RACES"
    if nextCupRace:
        header = (
            f"NEXT CUP RACE: {nextCupRace.get('raceName', '')} | "
            f"{countdown_to(nextCupRace['date'], nextCupRace.get('startTime', '00:00'))}"
        )

    return {
        "mode": "SCHEDULE",
        "header": header,
        "rows": rows[:10]
    }


# =========================
# IDLE MODE (POINTS + SCHEDULE)
# =========================

def build_idle_layout(standingsData, allSchedules):
    """
    Combined layout showing both points standings and upcoming schedule.
    This is displayed when there's no active race.
    """
    # Get top 10 drivers
    drivers = standingsData["drivers"][:10]
    
    # Get next 5 races
    now = datetime.now()
    upcomingRaces = []
    nextCupRace = None
    
    for sched in allSchedules:
        series = sched.get("series", "UNKNOWN")
        
        for race in sched.get("races", []):
            raceDt = datetime.fromisoformat(
                f"{race['date']} {race.get('startTime', '00:00')}"
            )
            
            if raceDt >= now:
                upcomingRaces.append({
                    "date": race["date"],
                    "time": race.get("startTime", ""),
                    "name": race.get("raceName", "UNKNOWN"),
                    "track": race.get("track", ""),
                    "location": race.get("location", ""),
                    "broadcast": race.get("broadcast", ""),
                    "series": series,
                    "isChase": race.get("isChase", False)
                })
                
                if series == "CUP" and nextCupRace is None:
                    nextCupRace = race
    
    upcomingRaces.sort(key=lambda r: (r["date"], r["time"]))
    
    # Build header with next Cup race info
    scheduleHeader = "UPCOMING RACES"
    if nextCupRace:
        scheduleHeader = (
            f"NEXT: {nextCupRace.get('raceName', '')} | "
            f"{countdown_to(nextCupRace['date'], nextCupRace.get('startTime', '00:00'))}"
        )
    
    return {
        "mode": "IDLE",
        "pointsHeader": "CUP SERIES POINTS STANDINGS",
        "drivers": drivers,
        "scheduleHeader": scheduleHeader,
        "races": upcomingRaces[:5]
    }