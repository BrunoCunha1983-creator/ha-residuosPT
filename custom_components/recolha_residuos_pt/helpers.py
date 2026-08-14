"""Schedule helper functions."""

from __future__ import annotations

from datetime import date, datetime, time, timedelta
from typing import Iterable

from homeassistant.util import dt as dt_util

from .const import WEEKDAYS


def merged_config(entry) -> dict:
    """Return config entry data merged with options."""
    data = dict(entry.data)
    data.update(entry.options)
    return data


def next_collection(days: Iterable[str], start: date | None = None) -> date | None:
    """Return next collection date, including today."""
    day_indexes = {WEEKDAYS[d] for d in days if d in WEEKDAYS}
    if not day_indexes:
        return None
    current = start or dt_util.now().date()
    for offset in range(0, 14):
        candidate = current + timedelta(days=offset)
        if candidate.weekday() in day_indexes:
            return candidate
    return None


def collections_between(days: Iterable[str], start: datetime, end: datetime) -> list[date]:
    """Expand recurring weekday schedule to dates in range."""
    day_indexes = {WEEKDAYS[d] for d in days if d in WEEKDAYS}
    if not day_indexes:
        return []
    result: list[date] = []
    current = start.date()
    last = end.date()
    while current <= last:
        event_start = datetime.combine(current, time.min, tzinfo=start.tzinfo)
        event_end = event_start + timedelta(days=1)
        if (
            current.weekday() in day_indexes
            and event_start < end
            and event_end > start
        ):
            result.append(current)
        current += timedelta(days=1)
    return result
