"""The Energy Mix Data integration."""

from __future__ import annotations

from pathlib import Path

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.const import CONF_DEVICE_ID

from .const import DOMAIN, CONF_TOPIC_PREFIX

# TODO List the platforms that you want to support.
# For your initial PR, limit it to 1 platform.
PLATFORMS = ["sensor"]


async def async_setup(hass, config):
    # Create the hass data entry
    if DOMAIN not in hass.data:
        hass.data[DOMAIN] = {}

    return True


# TODO Update entry annotation
async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    # Register the paths for the custom modules
    hass.http.register_static_path(
        "/ha-glow-files",
        hass.config.path("custom_components/ha-glow-integration/www"),
        cache_headers=False,
    )
    await hass.data["lovelace"]["resources"].async_create_item(
        {"res_type": "module", "url": "/ha-glow-files/chartjs-card.js"}
    )
    await hass.data["lovelace"]["resources"].async_create_item(
        {"res_type": "module", "url": "/ha-glow-files/glow-strategy.js"}
    )

    if entry.entry_id not in hass.data[DOMAIN]:
        hass.data[DOMAIN][entry.entry_id] = {}

    hass.data[DOMAIN][entry.entry_id][CONF_DEVICE_ID] = (
        entry.data[CONF_DEVICE_ID].strip().upper().replace(":", "").replace(" ", "")
    )
    hass.data[DOMAIN][entry.entry_id][CONF_TOPIC_PREFIX] = (
        entry.data.get(CONF_TOPIC_PREFIX, "glow")
        .strip()
        .replace("#", "")
        .replace(" ", "")
    )

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


# TODO Update entry annotation
async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    return True
