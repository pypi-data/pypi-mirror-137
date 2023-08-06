from datetime import datetime

from pytz import timezone


def as_JST(timestamp: datetime):
    """Convert timestamp to JST."""
    return timestamp.astimezone(timezone("Asia/Tokyo"))
