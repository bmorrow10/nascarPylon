import json
from pathlib import Path

DATA_DIR = Path("data")

def load_json(filename):
    with open(DATA_DIR / filename) as f:
        return json.load(f)

def load_all_schedules():
    schedules = []
    for fname in ["sched.json", "schedOR.json", "schedTruck.json"]:
        try:
            schedules.append(load_json(fname))
        except FileNotFoundError:
            pass
    return schedules