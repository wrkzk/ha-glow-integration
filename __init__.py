"""The Energy Mix Data integration."""

from __future__ import annotations

from pathlib import Path

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN

# TODO List the platforms that you want to support.
# For your initial PR, limit it to 1 platform.
PLATFORMS = ["sensor"]


# TODO Update entry annotation
async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


# TODO Update entry annotation
async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    return True


async def async_setup(hass, config):
    # path = Path(__file__).parent / "www"
    # utils.register_static_path(
    #    hass.http.app, "/energy_mix_data/www/chartjs-card.js", path / "chartjs-cardjs"
    # )

    hass.http.register_static_path(
        "/energy_mix_data_files",
        hass.config.path("custom_components/ha-glow-integration/www"),
        cache_headers=False,
    )

    await hass.data["lovelace"]["resources"].async_create_item(
        {"res_type": "module", "url": "/energy_mix_data_files/chartjs-card.js"}
    )

    await hass.data["lovelace"]["resources"].async_create_item(
        {"res_type": "module", "url": "/energy_mix_data_files/glow-strategy.js"}
    )

    await hass.data["lovelace"]["resources"].async_create_item(
        {"res_type": "module", "url": "/energy_mix_data_files/leaf.png"}
    )

    return True
