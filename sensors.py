from homeassistant.components.sensor import SensorDeviceClass, SensorStateClass
from homeassistant.const import (
    SIGNAL_STRENGTH_DECIBELS,
    UnitOfEnergy,
    UnitOfPower,
    UnitOfTemperature,
    UnitOfVolume,
)

STATE_SENSORS = [
    {
        "name": "Smart Meter IHD Software Version",
        "device_class": None,
        "unit_of_measurement": None,
        "state_class": None,
        # "entity_category": EntityCategory.DIAGNOSTIC,
        "icon": "mdi:information-outline",
        "func": lambda js: js["software"],
    },
    {
        "name": "Smart Meter IHD Hardware",
        "device_class": None,
        "unit_of_measurement": None,
        "state_class": None,
        # "entity_category": EntityCategory.DIAGNOSTIC,
        "icon": "mdi:information-outline",
        "func": lambda js: js["hardware"],
    },
    {
        "name": "Smart Meter IHD HAN Status",
        "device_class": None,
        "unit_of_measurement": None,
        "state_class": None,
        # "entity_category": EntityCategory.DIAGNOSTIC,
        "icon": "mdi:information-outline",
        "func": lambda js: js["han"]["status"],
    },
    {
        "name": "Smart Meter IHD HAN RSSI",
        "device_class": SensorDeviceClass.SIGNAL_STRENGTH,
        "unit_of_measurement": SIGNAL_STRENGTH_DECIBELS,
        "state_class": SensorStateClass.MEASUREMENT,
        # "entity_category": EntityCategory.DIAGNOSTIC,
        "icon": "mdi:wifi-strength-outline",
        "func": lambda js: js["han"]["rssi"],
    },
    {
        "name": "Smart Meter IHD HAN LQI",
        "device_class": None,
        "unit_of_measurement": None,
        "state_class": SensorStateClass.MEASUREMENT,
        # "entity_category": EntityCategory.DIAGNOSTIC,
        "icon": "mdi:wifi-strength-outline",
        "func": lambda js: js["han"]["lqi"],
    },
]

ELECTRICITY_SENSORS = [
    {
        "name": "Smart Meter Electricity: Export",
        "device_class": SensorDeviceClass.ENERGY,
        "unit_of_measurement": UnitOfEnergy.KILO_WATT_HOUR,
        "state_class": SensorStateClass.TOTAL_INCREASING,
        "icon": "mdi:flash",
        "func": lambda js: js["electricitymeter"]["energy"]["export"]["cumulative"],
    },
    {
        "name": "Smart Meter Electricity: Import",
        "device_class": SensorDeviceClass.ENERGY,
        "unit_of_measurement": UnitOfEnergy.KILO_WATT_HOUR,
        "state_class": SensorStateClass.TOTAL_INCREASING,
        "icon": "mdi:flash",
        "func": lambda js: js["electricitymeter"]["energy"]["import"]["cumulative"],
        "ignore_zero_values": True,
    },
    {
        "name": "Smart Meter Electricity: Import (Today)",
        "device_class": SensorDeviceClass.ENERGY,
        "unit_of_measurement": UnitOfEnergy.KILO_WATT_HOUR,
        "state_class": SensorStateClass.TOTAL_INCREASING,
        "icon": "mdi:flash",
        "func": lambda js: js["electricitymeter"]["energy"]["import"]["day"],
    },
    {
        "name": "Smart Meter Electricity: Import (This week)",
        "device_class": SensorDeviceClass.ENERGY,
        "unit_of_measurement": UnitOfEnergy.KILO_WATT_HOUR,
        "state_class": SensorStateClass.TOTAL_INCREASING,
        "icon": "mdi:flash",
        "func": lambda js: js["electricitymeter"]["energy"]["import"]["week"],
    },
    {
        "name": "Smart Meter Electricity: Import (This month)",
        "device_class": SensorDeviceClass.ENERGY,
        "unit_of_measurement": UnitOfEnergy.KILO_WATT_HOUR,
        "state_class": SensorStateClass.TOTAL_INCREASING,
        "icon": "mdi:flash",
        "func": lambda js: js["electricitymeter"]["energy"]["import"]["month"],
    },
    {
        "name": "Smart Meter Electricity: Import Unit Rate",
        "device_class": SensorDeviceClass.MONETARY,
        "unit_of_measurement": "GBP/kWh",
        "state_class": None,
        "icon": "mdi:cash",
        "func": lambda js: js["electricitymeter"]["energy"]["import"]["price"][
            "unitrate"
        ],
        "ignore_zero_values": True,
    },
    {
        "name": "Smart Meter Electricity: Import Standing Charge",
        "device_class": SensorDeviceClass.MONETARY,
        "unit_of_measurement": "GBP",
        "state_class": None,
        "icon": "mdi:cash",
        "func": lambda js: js["electricitymeter"]["energy"]["import"]["price"][
            "standingcharge"
        ],
        "ignore_zero_values": True,
    },
    {
        "name": "Smart Meter Electricity: Power",
        "device_class": SensorDeviceClass.POWER,
        "unit_of_measurement": UnitOfPower.KILO_WATT,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:flash",
        "func": lambda js: js["electricitymeter"]["power"]["value"],
    },
    {
        "name": "Smart Meter Electricity: Cost (Today)",
        "device_class": SensorDeviceClass.MONETARY,
        "unit_of_measurement": "GBP",
        "state_class": SensorStateClass.TOTAL,
        "icon": "mdi:cash",
        "func": lambda js: round(
            js["electricitymeter"]["energy"]["import"]["price"]["standingcharge"]
            + (
                js["electricitymeter"]["energy"]["import"]["day"]
                * js["electricitymeter"]["energy"]["import"]["price"]["unitrate"]
            ),
            2,
        ),
    },
]

THERMAL_SENSORS = [
    {
        "name": "Current Temperature",
        "device_class": SensorDeviceClass.TEMPERATURE,
        "unit_of_measurement": UnitOfTemperature.CELSIUS,
        "state_class": SensorStateClass.MEASUREMENT,
        "suggested_display_precision": 1,
        "icon": "mdi:thermometer",
        "func": lambda js, name, id: js[name][id]["temperature"]["value"],
        "ignore_zero_values": False,
        "thermal": True,
    },
    {
        "name": "Current Humidity",
        "device_class": SensorDeviceClass.HUMIDITY,
        "unit_of_measurement": "%",
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:water-percent",
        "func": lambda js, name, id: js[name][id]["humidity"]["value"],
        "ignore_zero_values": False,
        "thermal": True,
    },
    {
        "name": "Current Battery",
        "device_class": SensorDeviceClass.BATTERY,
        "unit_of_measurement": "%",
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:battery",
        "func": lambda js, name, id: js[name][id]["battery"]["value"],
        "ignore_zero_values": False,
        "thermal": True,
    },
    {
        "name": "Hardware Address",
        "device_class": None,
        "unit_of_measurement": None,
        "state_class": None,
        # "entity_category": EntityCategory.DIAGNOSTIC,
        "icon": "mdi:information-outline",
        "func": lambda js, name, id: ":".join(
            [id[i : i + 2] for i in range(0, len(id), 2)]
        ),
        "ignore_zero_values": False,
        "thermal": True,
    },
]

GAS_SENSORS = [
    {
        "name": "Smart Meter Gas: Import",
        "device_class": SensorDeviceClass.ENERGY,
        "unit_of_measurement": UnitOfEnergy.KILO_WATT_HOUR,
        "state_class": SensorStateClass.TOTAL_INCREASING,
        "icon": "mdi:fire",
        "func": lambda js: js["gasmeter"]["energy"]["import"]["cumulative"],
        "ignore_zero_values": True,
    },
    {
        "name": "Smart Meter Gas: Import Vol",
        "device_class": SensorDeviceClass.GAS,
        "unit_of_measurement": UnitOfVolume.CUBIC_METERS,
        "state_class": SensorStateClass.TOTAL_INCREASING,
        "icon": "mdi:fire",
        "func": lambda js: js["gasmeter"]["energy"]["import"]["cumulativevol"],
        "ignore_zero_values": True,
    },
    {
        "name": "Smart Meter Gas: Import Vol (Today)",
        "device_class": SensorDeviceClass.ENERGY,  # Change this to GAS if cubic meters is used
        "unit_of_measurement": UnitOfEnergy.KILO_WATT_HOUR,  # Might change to VOLUME_CUBIC_METERS soon
        "state_class": SensorStateClass.TOTAL_INCREASING,
        "icon": "mdi:fire",
        "func": lambda js: js["gasmeter"]["energy"]["import"]["dayvol"],
    },
    {
        "name": "Smart Meter Gas: Import Vol (This week)",
        "device_class": SensorDeviceClass.ENERGY,  # Change this to GAS if cubic meters is used
        "unit_of_measurement": UnitOfEnergy.KILO_WATT_HOUR,  # Might change to VOLUME_CUBIC_METERS soon
        "state_class": SensorStateClass.TOTAL_INCREASING,
        "icon": "mdi:fire",
        "func": lambda js: js["gasmeter"]["energy"]["import"]["weekvol"],
    },
    {
        "name": "Smart Meter Gas: Import Vol (This month)",
        "device_class": SensorDeviceClass.ENERGY,  # Change this to GAS if cubic meters is used
        "unit_of_measurement": UnitOfEnergy.KILO_WATT_HOUR,  # Might change to VOLUME_CUBIC_METERS soon
        "state_class": SensorStateClass.TOTAL_INCREASING,
        "icon": "mdi:fire",
        "func": lambda js: js["gasmeter"]["energy"]["import"]["monthvol"],
    },
    {
        "name": "Smart Meter Gas: Import (Today)",
        "device_class": SensorDeviceClass.ENERGY,
        "unit_of_measurement": UnitOfEnergy.KILO_WATT_HOUR,
        "state_class": SensorStateClass.TOTAL_INCREASING,
        "icon": "mdi:fire",
        "func": lambda js: js["gasmeter"]["energy"]["import"]["day"],
    },
    {
        "name": "Smart Meter Gas: Import (This week)",
        "device_class": SensorDeviceClass.ENERGY,
        "unit_of_measurement": UnitOfEnergy.KILO_WATT_HOUR,
        "state_class": SensorStateClass.TOTAL_INCREASING,
        "icon": "mdi:fire",
        "func": lambda js: js["gasmeter"]["energy"]["import"]["week"],
    },
    {
        "name": "Smart Meter Gas: Import (This month)",
        "device_class": SensorDeviceClass.ENERGY,
        "unit_of_measurement": UnitOfEnergy.KILO_WATT_HOUR,
        "state_class": SensorStateClass.TOTAL_INCREASING,
        "icon": "mdi:fire",
        "func": lambda js: js["gasmeter"]["energy"]["import"]["month"],
    },
    {
        "name": "Smart Meter Gas: Import Unit Rate",
        "device_class": SensorDeviceClass.MONETARY,
        "unit_of_measurement": "GBP/kWh",
        "state_class": None,
        "icon": "mdi:cash",
        "func": lambda js: js["gasmeter"]["energy"]["import"]["price"]["unitrate"],
        "ignore_zero_values": True,
    },
    {
        "name": "Smart Meter Gas: Import Standing Charge",
        "device_class": SensorDeviceClass.MONETARY,
        "unit_of_measurement": "GBP",
        "state_class": None,
        "icon": "mdi:cash",
        "func": lambda js: js["gasmeter"]["energy"]["import"]["price"][
            "standingcharge"
        ],
        "ignore_zero_values": True,
    },
    # Removed June 2022 in IHD software update 1.8.13
    # {
    #   "name": "Smart Meter Gas: Power",
    #   "device_class": SensorDeviceClass.POWER,
    #   "unit_of_measurement": UnitOfPower.KILO_WATT,
    #   "state_class": SensorStateClass.MEASUREMENT,
    #   "icon": "mdi:fire",
    #   "func": lambda js : js['gasmeter']['power']['value'],
    # },
    {
        "name": "Smart Meter Gas: Cost (Today)",
        "device_class": SensorDeviceClass.MONETARY,
        "unit_of_measurement": "GBP",
        "state_class": SensorStateClass.TOTAL,
        "icon": "mdi:cash",
        "func": lambda js: round(
            (js["gasmeter"]["energy"]["import"]["price"]["standingcharge"] or 0)
            + (
                (js["gasmeter"]["energy"]["import"]["day"] or 0)
                * (js["gasmeter"]["energy"]["import"]["price"]["unitrate"] or 0)
            ),
            2,
        ),
    },
]
