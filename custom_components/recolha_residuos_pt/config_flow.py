"""Config flow for Recolha de Resíduos Portugal."""

from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers.selector import (
    SelectOptionDict,
    SelectSelector,
    SelectSelectorConfig,
    SelectSelectorMode,
    TextSelector,
    TextSelectorConfig,
)

from .const import (
    CONF_LOCALITY,
    CONF_MUNICIPALITY,
    CONF_OPERATOR,
    CONF_SCHEDULES,
    DOMAIN,
    OPERATORS,
    WEEKDAY_LABELS,
    WASTE_STREAMS,
)


def _weekday_selector(default: list[str] | None = None):
    return SelectSelector(
        SelectSelectorConfig(
            options=[
                SelectOptionDict(value=value, label=label)
                for value, label in WEEKDAY_LABELS.items()
            ],
            multiple=True,
            mode=SelectSelectorMode.DROPDOWN,
        )
    )


def _schedule_schema(defaults: dict[str, list[str]] | None = None) -> vol.Schema:
    defaults = defaults or {}
    fields: dict[Any, Any] = {}
    for stream_id, stream in WASTE_STREAMS.items():
        fields[
            vol.Optional(
                stream_id,
                default=defaults.get(stream_id, []),
                description={"suggested_value": defaults.get(stream_id, [])},
            )
        ] = _weekday_selector(defaults.get(stream_id, []))
    return vol.Schema(fields)


class RecolhaResiduosPTConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow."""

    VERSION = 1

    def __init__(self) -> None:
        self._data: dict[str, Any] = {}

    async def async_step_user(self, user_input: dict[str, Any] | None = None) -> FlowResult:
        """Handle initial configuration."""
        if user_input is not None:
            self._data.update(user_input)
            return await self.async_step_schedule()

        operator_options = [
            SelectOptionDict(value=value, label=label)
            for value, label in OPERATORS.items()
        ]
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_MUNICIPALITY): TextSelector(
                        TextSelectorConfig(autocomplete="address-level2")
                    ),
                    vol.Optional(CONF_LOCALITY, default=""): TextSelector(
                        TextSelectorConfig(autocomplete="address-level3")
                    ),
                    vol.Required(CONF_OPERATOR, default="other"): SelectSelector(
                        SelectSelectorConfig(
                            options=operator_options,
                            mode=SelectSelectorMode.DROPDOWN,
                        )
                    ),
                }
            ),
        )

    async def async_step_schedule(self, user_input: dict[str, Any] | None = None) -> FlowResult:
        """Configure weekly collection schedules."""
        if user_input is not None:
            self._data[CONF_SCHEDULES] = user_input
            title = self._data[CONF_MUNICIPALITY]
            locality = self._data.get(CONF_LOCALITY)
            if locality:
                title = f"{locality} — {title}"
            return self.async_create_entry(title=title, data=self._data)

        return self.async_show_form(step_id="schedule", data_schema=_schedule_schema())

    @staticmethod
    def async_get_options_flow(config_entry):
        """Return options flow."""
        return RecolhaResiduosPTOptionsFlow(config_entry)


class RecolhaResiduosPTOptionsFlow(config_entries.OptionsFlow):
    """Handle options."""

    def __init__(self, config_entry) -> None:
        self.config_entry = config_entry

    async def async_step_init(self, user_input: dict[str, Any] | None = None) -> FlowResult:
        """Manage weekly schedules."""
        current = self.config_entry.options.get(
            CONF_SCHEDULES, self.config_entry.data.get(CONF_SCHEDULES, {})
        )
        if user_input is not None:
            return self.async_create_entry(title="", data={CONF_SCHEDULES: user_input})

        return self.async_show_form(
            step_id="init",
            data_schema=_schedule_schema(current),
        )
