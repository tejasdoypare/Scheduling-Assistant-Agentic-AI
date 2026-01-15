from datetime import datetime
from zoneinfo import ZoneInfo

def to_utc(local_dt_str: str, timezone: str) -> datetime:
    local_dt = datetime.fromisoformat(local_dt_str)
    local_dt = local_dt.replace(tzinfo=ZoneInfo(timezone))
    return local_dt.astimezone(ZoneInfo("UTC"))
