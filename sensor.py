"""Platform for sensor integration."""

from __future__ import annotations

from datetime import timedelta
import logging

import aiohttp

from homeassistant.components.sensor import SensorEntity, SensorStateClass
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config: ConfigType,
    async_add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Set up the sensor platform."""

    coordinator = MyEnergyCoordinator(
        hass,
        config,
    )
    await coordinator.async_config_entry_first_refresh()

    sensors = coordinator.topics

    async_add_entities(
        [
            BaseEnergySensor(
                coordinator,
                sensor,
                coordinator.data["response"][sensors.index(sensor)]["perc"],
                sensors.index(sensor),
            )
            for sensor in sensors
        ]
    )


class MyEnergyCoordinator(DataUpdateCoordinator):
    """My custom coordinator."""

    def __init__(self, hass, config) -> None:
        """Initialize my coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name="energy_sensor",
            update_interval=timedelta(seconds=30),
            always_update=True,
        )
        self.hass = hass
        self.config = config
        self.current_power = 100
        self.count = 0
        self.topics = []

    async def _async_update_data(self):
        region_id = 13  # London region id
        async with (
            aiohttp.ClientSession() as session,
            session.get(
                "https://api.carbonintensity.org.uk/regional/regionid/" + str(region_id)
            ) as mix_resp,
            session.get(
                "https://api.carbonintensity.org.uk/intensity/factors"
            ) as factor_resp,
        ):
            mix_json_resp = await mix_resp.json()
            factor_json_resp = await factor_resp.json()

            for item in mix_json_resp["data"][0]["data"][0]["generationmix"]:
                if item["fuel"] not in self.topics:
                    self.topics.append(item["fuel"])

            for key in factor_json_resp["data"][0]:
                if key + "-carbon" not in self.topics:
                    self.topics.append(key + "-carbon")

            return {
                "response": mix_json_resp["data"][0]["data"][0]["generationmix"]
                + [
                    {"perc": value, "fuel": key, "carbon": True}
                    for (key, value) in factor_json_resp["data"][0].items()
                ]
            }


class BaseEnergySensor(CoordinatorEntity, SensorEntity):
    """Representation of a Sensor."""

    def __init__(self, coordinator, name, value, entry):
        super().__init__(coordinator, context=value)
        self._attr_name = name
        self._attr_native_unit_of_measurement = "%"
        self._attr_device_class = None
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_suggested_display_precision = 3
        self._attr_native_value = value
        self.data_entry = entry

    @callback
    def _handle_coordinator_update(self) -> None:
        if "carbon" in self.coordinator.data["response"][self.data_entry]:
            self._attr_native_unit_of_measurement = "gCO2/kWh"

        self._attr_native_value = str(
            self.coordinator.data["response"][self.data_entry]["perc"]
        )
        self._attr_name = self.coordinator.data["response"][self.data_entry]["fuel"]
        self.async_write_ha_state()
