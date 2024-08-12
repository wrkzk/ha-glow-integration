# Home Assistant Integration for Hildebrand Glow Hub
This integration exposes sensor entities that fetch data via MQTT from your smart meterm. Additionally, this integration fetches public data from the internet, providing further insights into your energy consumption. Bundled with this integration is a custom Glow dashboard for Home assistant, as well as access to the custom cards used for the dashboard for use in your own dashboards. See the images below.

![Custom Integration Dashboard](./ha-dashboard.png)

# Installation
## 1. Requirements
- A working Home Assistant installation
- Hildebrand Glow CAD linked to a working smart meter, connected to the same wireless network as your HA host
- Mosquitto Broker installed as an add-on to Home Assistant (see [here](https://github.com/home-assistant/addons/blob/master/mosquitto/DOCS.md))
- MQTT Integration installed and configured to point to the Mosquitto Broker (see [here](https://www.home-assistant.io/integrations/mqtt/))

## 2. Set up HACS

## 3. Add custom HACS repository
