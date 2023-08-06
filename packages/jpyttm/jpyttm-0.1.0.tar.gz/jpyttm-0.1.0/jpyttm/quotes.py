import datetime
import re
import time
from datetime import timedelta
from decimal import Decimal
from typing import Dict, List, Optional, Tuple

import requests
from bs4 import BeautifulSoup

from .calendar import as_JST
from .constants import (
    BASE_URL,
    CURRENCY_REGEX,
    MAX_RETRY,
    NO_DATA,
    OPTIONS,
    RESULTS,
    SHIFT_JIS,
    TTM,
    YEAR_MONTH_DAY,
)


def get_options(
    timestamp_from: datetime.datetime, timestamp_to: datetime.datetime, retry: int = 5
) -> Tuple[datetime.datetime, Dict[str, int]]:
    """Get currency options."""
    params = YEAR_MONTH_DAY.format(
        **{
            "year": timestamp_to.year,
            "month": timestamp_to.month,
            "day": timestamp_to.day,
        }
    )
    response = requests.get(f"{BASE_URL}/{OPTIONS}?{params}")
    if response.status_code == 200:
        data = response.content.decode(SHIFT_JIS)
        if NO_DATA in data:
            timestamp_to -= timedelta(days=1)
            if timestamp_to >= timestamp_from:
                return get_options(timestamp_from, timestamp_to, retry=retry)
        else:
            currencies = {}
            for d in data.split("new Option"):
                match = re.match(CURRENCY_REGEX, d)
                if match:
                    currencies[match.group(1)] = int(match.group(2))
            return timestamp_to, currencies
    else:
        retry -= 1
        time.sleep(MAX_RETRY - retry)
        return get_options(timestamp_from, timestamp_to, retry=retry)


def get_ttm(date: datetime.date, currency: int, retry: int = 5) -> Decimal:
    """Get JPY TTM rates for currency."""
    params = YEAR_MONTH_DAY.format(
        **{"year": date.year, "month": date.month, "day": date.day}
    )
    response = requests.get(f"{BASE_URL}/{RESULTS}?{params}&c={currency}")
    if response.status_code == 200:
        data = response.content.decode(SHIFT_JIS)
        soup = BeautifulSoup(data, "lxml")
        table = soup.select("table.data-table5")
        assert len(table) == 1
        header = soup.select("table.data-table5 > tr > th")
        data = soup.select("table.data-table5 > tr > td")
        assert len(header) == 6
        assert len(data) == 6
        return dict(zip([h.text for h in header], [d.text for d in data]))[TTM]
    else:
        retry -= 1
        time.sleep(MAX_RETRY - retry)
        return get_ttm(date, currency, retry=retry)


def get_historical_ttm(
    currency: str,
    timestamp_from: Optional[datetime.datetime] = None,
    timestamp_to: Optional[datetime.datetime] = None,
) -> List[Tuple[datetime.date, Decimal]]:
    """Get historical JPY TTM rates for currency."""
    quotes = []
    now = datetime.datetime.utcnow()
    one_week_ago = now - timedelta(days=7)
    timestamp_from = as_JST(timestamp_from) if timestamp_from else as_JST(one_week_ago)
    timestamp_to = as_JST(timestamp_to) if timestamp_to else as_JST(now)
    while timestamp_to >= timestamp_from:
        date = timestamp_to.date()
        result = get_options(timestamp_from, timestamp_to)
        # May exceed bounds, b/c of holidays
        if result is not None:
            timestamp_to, currencies = result
            if currency in currencies:
                quote = get_ttm(timestamp_to, currencies[currency])
                quotes.append((date, Decimal(quote)))
        else:
            break
        timestamp_to -= timedelta(days=1)
    return reversed(quotes)
