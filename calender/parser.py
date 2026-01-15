import json

REQUIRED_KEYS = [
    "user_id", "timezone", "working_hours", "preferences", "events"
]

def load_calendar(path: str) -> dict:
    with open(path, "r") as f:
        data = json.load(f)

    for key in REQUIRED_KEYS:
        if key not in data:
            raise ValueError(f"Missing key: {key}")

    return data
