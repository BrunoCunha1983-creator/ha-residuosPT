"""Calendar for Recolha de Resíduos Portugal."""

from __future__ import annotations

from datetime import date, datetime, timedelta

from homeassistant.components.calendar import CalendarEntity, CalendarEvent
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import CONF_SCHEDULES, DOMAIN, WASTE_STREAMS
from .helpers import collections_between, merged_config, next_collection


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up calendar."""
    async_add_entities([WasteCalendar(entry)])


class WasteCalendar(CalendarEntity):
    """Combined waste collection calendar."""

    _attr_has_entity_name = True
    _attr_name = "Calendário de recolhas"
    _attr_icon = "mdi:calendar"

    def __init__(self, entry: ConfigEntry) -> None:
        self.entry = entry
        self._attr_unique_id = f"{entry.entry_id}_calendar"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name=f"Recolha de Resíduos — {entry.title}",
            manufacturer="Portugal / Operador local",
            model="Calendário de recolha seletiva",
        )

    @property
    def event(self) -> CalendarEvent | None:
        """Return the next upcoming collection event."""
        cfg = merged_config(self.entry)
        schedules = cfg.get(CONF_SCHEDULES, {})
        candidates: list[tuple[date, str]] = []
        for stream_id, stream in WASTE_STREAMS.items():
            when = next_collection(schedules.get(stream_id, []))
            if when:
                candidates.append((when, stream_id))
        if not candidates:
            return None
        when, stream_id = min(candidates, key=lambda item: item[0])
        stream = WASTE_STREAMS[stream_id]
        return CalendarEvent(
            start=when,
            end=when + timedelta(days=1),
            summary=f"Recolha {stream['short_name']} — {stream['material']}",
            description=f"Contentor {stream['color']}. {stream['material']}",
        )

    async def async_get_events(
        self,
        hass: HomeAssistant,
        start_date: datetime,
        end_date: datetime,
    ) -> list[CalendarEvent]:
        """Return events in a datetime range."""
        cfg = merged_config(self.entry)
        schedules = cfg.get(CONF_SCHEDULES, {})
        events: list[CalendarEvent] = []
        for stream_id, stream in WASTE_STREAMS.items():
            for when in collections_between(
                schedules.get(stream_id, []), start_date, end_date
            ):
                events.append(
                    CalendarEvent(
                        start=when,
                        end=when + timedelta(days=1),
                        summary=f"Recolha {stream['short_name']} — {stream['material']}",
                        description=(
                            f"Contentor {stream['color']} ({stream['hex']}). "
                            f"{stream['material']}"
                        ),
                    )
                )
        return sorted(events, key=lambda event: event.start)
