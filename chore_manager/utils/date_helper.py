from datetime import datetime, timezone


def get_today_date() -> str:
    today = datetime.now(timezone.utc)
    return today.strftime("%Y-%m-%d")
