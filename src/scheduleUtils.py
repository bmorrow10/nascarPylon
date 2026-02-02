# src/scheduleUtils.py

from datetime import datetime, timedelta
from pathlib import Path
import json

DATA_DIR = Path("data")


def load_schedule(filename):
    with open(DATA_DIR / filename) as f:
        return json.load(f)


def parse_race_datetime(race):
    """
    Convert race date + startTime into a datetime object.
    Assumes local time (ET) for now.
    """
    return datetime.fromisoformat(
        f"{race['date']} {race['startTime']}"
    )


def find_next_cup_race():
    """
    Returns the next upcoming CUP race only.
    """
    sched = load_schedule("sched.json")
    now = datetime.now()

    upcoming = []

    for race in sched["races"]:
        raceDt = parse_race_datetime(race)
        if raceDt > now:
            upcoming.append((raceDt, race))

    if not upcoming:
        return None

    upcoming.sort(key=lambda x: x[0])
    return upcoming[0]  # (datetime, race)


def countdown_to(dateStr, timeStr="00:00"):
    raceDt = datetime.fromisoformat(f"{dateStr} {timeStr}")
    now = datetime.now()

    if raceDt < now:
        return "RACE STARTED"

    delta = raceDt - now
    days = delta.days
    hours, rem = divmod(delta.seconds, 3600)
    minutes = rem // 60

    if days > 0:
        return f"{days}d {hours}h {minutes}m"
    return f"{hours}h {minutes}m"
