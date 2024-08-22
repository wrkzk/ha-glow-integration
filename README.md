# Home Assistant Integration for Hildebrand Glow Hub
This integration exposes sensor entities that fetch data via MQTT from your smart meter. Additionally, this integration fetches public data from the internet, providing further insights into your energy consumption. Bundled with this integration is a custom Glow dashboard for Home assistant, as well as access to the custom cards used for the dashboard for use in your own dashboards. See the images below.

![image](https://github.com/user-attachments/assets/5622d95e-fd3f-4991-938c-e7f1e2f1a6b7)

# Installation
## 1. Requirements
- A working Home Assistant installation
- Hildebrand Glow IHD linked to a working smart meter, connected to the same wireless network as your HA host
- Mosquitto Broker installed as an add-on to Home Assistant (see [here](https://github.com/home-assistant/addons/blob/master/mosquitto/DOCS.md))
  - Be sure that the username and password of your Home Assistant account (which is used as the broker authentication) matches the username and password entered in the MQTT configuration of your Hildebrand Glow IHD
  - You can also specify a new username and password in the Mosquitto Broker configuration (see [here](https://github.com/home-assistant/addons/blob/master/mosquitto/DOCS.md#option-logins-optional))
- MQTT Integration installed and configured to point to the Mosquitto Broker (see [here](https://www.home-assistant.io/integrations/mqtt/))
  - The MQTT Integration should automatically detect that the Mosquitto Broker is installed and automatically set the correct configuration

## 2. Set up HACS
Follow the steps outline on the [HACS installation page](https://hacs.xyz/docs/use/download/download/). Be sure to select the OS/Supervised tab, and follow the instructions, including installing the add-on and all the following steps. Once the add-on logs show installation finished, reboot the machine running Home Assistant, and reconnect. Then follow the steps [here](https://hacs.xyz/docs/use/configuration/basic/) to set up the HACS integration. Once the HACS integration is installed, you should see a new **HACS** tab on the left sidebar.

## 3. Add custom HACS repository
Navigate to the newly created HACS page on the sidebar, and click on **Custom repositories** as shown below.

![Custom repositories](https://github.com/user-attachments/assets/e0445598-0787-4f0a-bd49-0fd5ab036314)

In the dialog box that pops up, enter the repository URL, `https://github.com/wrkzk/ha-glow-integration`. Select **Integration** for the category, then click **Add**.

![image](https://github.com/user-attachments/assets/280ed5de-d0ed-4021-975c-74f61b48fcf1)

Now, type the name of the integration, `ha-glow-integration`, into the searchbar on the HACS page. Click the three dots on the right side of the integration that appears, and click **Download** as shown below. Click the dialog box that appears to confirm that you want to download the integration. After downloading the integration, restart Home Assistant one more time to complete the download.

![image](https://github.com/user-attachments/assets/4025d5d7-daf5-4b9e-867c-3435818bc3f1)

## 4. Install the Integration

Finally, navigate to **Settings** > **Devices & Services** and click the **Add Integration** button in the bottom right. Type the name of the integration, `ha-glow-integration`, into the search bar, and click the integration that should come up. Assuming you set up the MQTT stream correctly, and left the MQTT topic on the IHD device as `glow`, you should not have to change the default options on the setup box. Click **Submit**, and the integration should be installed. You should see the all the sensor entities, including the thermal sensors as seperate devices, appear as soon as the next MQTT update is published.

# Enabling the Custom Dashboard
- To enable the custom dashboard, first navigate to **Settings** > **Dashboards** and click **Add Dashboard** in the bottom right. Select **New dashboard from scratch**. Give this dashboard a title that you want, such as `Glow`, any icon, leave the url as it is, and then click **Create**.
- Now, navigate to this new dashboard on the left sidebar in the Home Assistant UI. Select the pencil icon in the top right, then the three dots, and select **Raw configuration editor**. In the text editor that appears, enter the following:
  ```
  strategy:
    type: custom:glow
  ```
  Select **Save** in the top right, and then close out once the configuration has saved. You should now see the custom Glow dashboard loaded. The cards that appear can also be used in other dashboard.

# Credits
- @megakid for his integration, which this one takes a lot of code parsing the MQTT stream from
