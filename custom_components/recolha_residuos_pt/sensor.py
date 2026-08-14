"""Sensors for Recolha de Resíduos Portugal."""

from __future__ import annotations

from datetime import date

from homeassistant.components.sensor import SensorDeviceClass, SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (
    CONF_LOCALITY,
    CONF_MUNICIPALITY,
    CONF_OPERATOR,
    CONF_SCHEDULES,
    DOMAIN,
    OPERATORS,
    WASTE_STREAMS,
    WEEKDAY_LABELS,
)
from .helpers import merged_config, next_collection


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up sensors."""
    entities = [WasteCollectionSensor(entry, stream_id) for stream_id in WASTE_STREAMS]
    entities.append(NextOverallCollectionSensor(entry))
    async_add_entities(entities)


class WasteBaseSensor(SensorEntity):
    """Base entity."""

    _attr_has_entity_name = True

    def __init__(self, entry: ConfigEntry) -> None:
        self.entry = entry
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name=f"Recolha de Resíduos — {entry.title}",
            manufacturer="Portugal / Operador local",
            model="Calendário de recolha seletiva",
        )

    @property
    def _config(self) -> dict:
        return merged_config(self.entry)


class WasteCollectionSensor(WasteBaseSensor):
    """Next collection for one waste stream."""

    _attr_device_class = SensorDeviceClass.DATE

    def __init__(self, entry: ConfigEntry, stream_id: str) -> None:
        super().__init__(entry)
        self.stream_id = stream_id
        stream = WASTE_STREAMS[stream_id]
        self._attr_unique_id = f"{entry.entry_id}_{stream_id}_next"
        self._attr_name = f"Próxima recolha — {stream['name']}"
        self._attr_icon = stream["icon"]

    @property
    def native_value(self) -> date | None:
        schedules = self._config.get(CONF_SCHEDULES, {})
        return next_collection(schedules.get(self.stream_id, []))

    @property
    def extra_state_attributes(self) -> dict:
        cfg = self._config
        stream = WASTE_STREAMS[self.stream_id]
        days = cfg.get(CONF_SCHEDULES, {}).get(self.stream_id, [])
        return {
            "contentor": stream["short_name"],
            "cor": stream["color"],
            "cor_hex": stream["hex"],
            "tipo_residuo": stream["material"],
            "dias_recolha": [WEEKDAY_LABELS[d] for d in days if d in WEEKDAY_LABELS],
            "municipio": cfg.get(CONF_MUNICIPALITY),
            "localidade": cfg.get(CONF_LOCALITY) or None,
            "operador": OPERATORS.get(cfg.get(CONF_OPERATOR), cfg.get(CONF_OPERATOR)),
            "colocar": stream["put"],
            "nao_colocar": stream["avoid"],
        }


class NextOverallCollectionSensor(WasteBaseSensor):
    """Next collection across all streams."""

    _attr_icon = "mdi:calendar-clock"

    def __init__(self, entry: ConfigEntry) -> None:
        super().__init__(entry)
        self._attr_unique_id = f"{entry.entry_id}_next_overall"
        self._attr_name = "Próxima recolha"

    @property
    def native_value(self) -> str | None:
        schedules = self._config.get(CONF_SCHEDULES, {})
        candidates: list[tuple[date, str]] = []
        for stream_id, stream in WASTE_STREAMS.items():
            when = next_collection(schedules.get(stream_id, []))
            if when:
                candidates.append((when, stream["short_name"]))
        if not candidates:
            return None
        next_date = min(item[0] for item in candidates)
        streams = [name for when, name in candidates if when == next_date]
        return f"{next_date.isoformat()} — {', '.join(streams)}"

    @property
    def extra_state_attributes(self) -> dict:
        schedules = self._config.get(CONF_SCHEDULES, {})
        upcoming = []
        for stream_id, stream in WASTE_STREAMS.items():
            when = next_collection(schedules.get(stream_id, []))
            if when:
                upcoming.append(
                    {
                        "data": when.isoformat(),
                        "contentor": stream["short_name"],
                        "cor": stream["color"],
                    }
                )
        upcoming.sort(key=lambda item: item["data"])
        return {"proximas": upcoming}
