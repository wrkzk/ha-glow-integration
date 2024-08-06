"""Platform for sensor integration."""

from __future__ import annotations

from datetime import timedelta
import json
import logging
import re
from typing import Iterable

import aiohttp

from homeassistant.components import mqtt
from homeassistant.components.mqtt.models import ReceiveMessage
from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.const import (
    ATTR_DEVICE_ID,
    CONF_DEVICE_ID,
    SIGNAL_STRENGTH_DECIBELS,
    UnitOfEnergy,
    UnitOfPower,
    UnitOfTemperature,
    UnitOfVolume,
)
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity import DeviceInfo, EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)
from homeassistant.util import slugify

from .const import CONF_TOPIC_PREFIX, DOMAIN
from .sensors import STATE_SENSORS, ELECTRICITY_SENSORS, THERMAL_SENSORS, GAS_SENSORS

_LOGGER = logging.getLogger(__name__)

device_types = {}


async def async_setup_entry(
    hass: HomeAssistant,
    config,
    async_add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Set up the sensor platform."""

    device_mac = hass.data[DOMAIN][config.entry_id][CONF_DEVICE_ID]
    topic_prefix = hass.data[DOMAIN][config.entry_id][CONF_TOPIC_PREFIX] or "glow"
    deviceUpdateGroups = {}
    thermal_sensor_ids = []

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

    @callback
    async def mqtt_message_received(message: ReceiveMessage):
        """Handle received MQTT message."""
        topic = message.topic
        payload = message.payload
        device_id = topic.split("/")[1]

        if len(topic.split("/")) >= 5:
            if topic.split("/")[3][0:12] == "glowsensorth":
                thermal_sensor_ids.append(topic.split("/")[4])
                device_id = topic.split("/")[3] + "/" + topic.split("/")[4]

        if device_mac == "+" or device_id == device_mac:
            updateGroups = await async_get_device_groups(
                deviceUpdateGroups, async_add_entities, device_id
            )
            _LOGGER.debug("Received message: %s", topic)
            _LOGGER.debug("  Payload: %s", payload)
            for updateGroup in updateGroups:
                updateGroup.process_update(message)

    data_topic = f"{topic_prefix}/#"

    await mqtt.async_subscribe(hass, data_topic, mqtt_message_received, 1)


def num_of_thermal_sensors() -> int:
    count = 0
    for value in device_types.values():
        if len(value) > 1:
            count += 1
    return count


async def async_get_device_groups(deviceUpdateGroups, async_add_entities, device_id):
    # add to update groups if not already there
    if device_id not in deviceUpdateGroups:
        _LOGGER.debug("New device found: %s", device_id)

        groups = []

        if device_id.split("/")[0] == "glowsensorth1":
            device_types[device_id.split("/")[1]] = [
                "Hildebrand Thermal Sensor " + str(num_of_thermal_sensors() + 1),
                device_id.split("/")[0],
            ]
            groups = [
                HildebrandGlowMqttSensorUpdateGroup(
                    device_id.split("/")[1],
                    device_id.split("/")[1],
                    THERMAL_SENSORS,
                ),
            ]

        else:
            device_types[device_id] = ["Hildebrand Glow Hub"]
            groups = [
                HildebrandGlowMqttSensorUpdateGroup(device_id, "STATE", STATE_SENSORS),
                HildebrandGlowMqttSensorUpdateGroup(
                    device_id, "electricitymeter", ELECTRICITY_SENSORS
                ),
                # HildebrandGlowMqttSensorUpdateGroup(device_id, "gasmeter", GAS_SENSORS),
            ]

        async_add_entities(
            [
                sensorEntity
                for updateGroup in groups
                for sensorEntity in updateGroup.all_sensors
            ],
            # True
        )
        deviceUpdateGroups[device_id] = groups

    return deviceUpdateGroups[device_id]


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


class HildebrandGlowMqttSensorUpdateGroup:
    """Representation of Hildebrand Glow MQTT Meter Sensors that all get updated together."""

    def __init__(self, device_id: str, topic_regex: str, meters: Iterable) -> None:
        """Initialize the sensor collection."""
        self._topic_regex = re.compile(topic_regex)
        self._sensors = [
            HildebrandGlowMqttSensor(device_id=device_id, **meter) for meter in meters
        ]

    def process_update(self, message: ReceiveMessage) -> None:
        """Process an update from the MQTT broker."""
        topic = message.topic
        payload = message.payload
        if self._topic_regex.search(topic):
            _LOGGER.debug("Matched on %s", self._topic_regex.pattern)
            parsed_data = json.loads(payload)
            for sensor in self._sensors:
                sensor.process_update(parsed_data)

    @property
    def all_sensors(self) -> Iterable[HildebrandGlowMqttSensor]:
        """Return all meters."""
        return self._sensors


class HildebrandGlowMqttSensor(SensorEntity):
    """Representation of a room sensor that is updated via MQTT."""

    def __init__(
        self,
        device_id,
        name,
        icon,
        device_class,
        unit_of_measurement,
        state_class,
        func,
        thermal=False,
        entity_category=None,
        ignore_zero_values=False,
        suggested_display_precision=None,
    ) -> None:
        """Initialize the sensor."""
        self._device_id = device_id
        self._ignore_zero_values = ignore_zero_values
        self._attr_suggested_display_precision = suggested_display_precision
        self._attr_name = name
        self._attr_unique_id = slugify(device_id + "_" + name)
        self._attr_icon = icon
        if device_class:
            self._attr_device_class = device_class
        if unit_of_measurement:
            self._attr_native_unit_of_measurement = unit_of_measurement
        if state_class:
            self._attr_state_class = state_class
        self._attr_entity_category = entity_category
        self._attr_should_poll = False

        self._func = func
        self._thermal = thermal

        if self._thermal:
            self._attr_device_info = DeviceInfo(
                connections={("mac", device_id)},
                manufacturer="Hildebrand Technology Limited",
                model="Glow Thermal Sensor",
                name=device_types[device_id][0],
            )
        else:
            self._attr_device_info = DeviceInfo(
                connections={("mac", device_id)},
                manufacturer="Hildebrand Technology Limited",
                model="Glow Smart Hub",
                name=device_types[device_id][0] + " " + device_id,
            )

        self._attr_native_value = None

    def process_update(self, mqtt_data) -> None:
        """Update the state of the sensor."""
        if self._thermal:
            new_value = self._func(
                mqtt_data, device_types[self._device_id][1], self._device_id
            )
        else:
            new_value = self._func(mqtt_data)

        if self._ignore_zero_values and new_value == 0:
            _LOGGER.debug(
                "Ignored new value of %s on %s.", new_value, self._attr_unique_id
            )
            return
        self._attr_native_value = new_value
        if (
            self.hass is not None
        ):  # this is a hack to get around the fact that the entity is not yet initialized at first
            self.async_schedule_update_ha_state()

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        return {ATTR_DEVICE_ID: self._device_id}
