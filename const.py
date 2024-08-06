"""Constants for the Energy Mix Data integration."""

DOMAIN = "energy_mix_data"
CONF_TOPIC_PREFIX = "topic_prefix"

ATTR_NAME = "name"
ATTR_ACTIVITY = "activity"
ATTR_BATTERY_STATE = "battery_state"
ATTR_RF_LINK_LEVEL = "rf_link_level"
ATTR_RF_LINK_STATE = "rf_link_state"
ATTR_SERIAL = "serial"
ATTR_OPERATING_HOURS = "operating_hours"
ATTR_LAST_ERROR = "last_error"
ATTR_ERROR = "error"
ATTR_STATE = "state"

URL_BASE = "/energy_mix_data"
MIX_CARDS = [
    {"name": "Energy Mix Card", "filename": "chartjs-card.js", "version": "1.1.1"}
]
