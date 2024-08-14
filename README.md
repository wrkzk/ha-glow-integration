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
Follow the steps outline on the [HACS installation page](https://hacs.xyz/docs/setup/prerequisites). You first need to enable advanced mode by turning on **Profile > User settings > Advanced mode**. Second, install an ssh addon, so that you can get terminal access through Home Assitant. Then run the script shown on the HACS installation page- be sure to use the OS/Supervised script.

## 3. Add custom HACS repository
Navigate to the newly created HACS page on the sidebar, and click on **Custom repositories** as shown below.

![Custom repositories](https://github.com/user-attachments/assets/e0445598-0787-4f0a-bd49-0fd5ab036314)

In the dialog box that pops up, enter the repository URL, `https://github.com/wrkzk/ha-glow-integration`. Select **Integration** for the category, then click **Add**.

![image](https://github.com/user-attachments/assets/280ed5de-d0ed-4021-975c-74f61b48fcf1)
