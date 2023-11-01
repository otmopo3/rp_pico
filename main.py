import utime
import wifi_network_module
import time_module
import led_module
import temperature_module
import settings_module
import machine
import _thread

import asyncio
import sys
from webserver.webserver_module import Webserver

from mqtt_module import HaMqttPublisher


def sync_temperature_thread(a, settings):
    # settings = settings_module.load_settings()

    ha_client = HaMqttPublisher(settings.mqtt_broker)

    ha_client.publish_config()

    while True:
        temperature_module.log_temperature()
        temperature = temperature_module.get_temperature()
        ha_client.publish_temperature(temperature)
        utime.sleep(300)
        led_module.led_toggle()


async def main():
    settings = settings_module.load_settings()

    wifi_network_module.connect_wifi(
        settings.wifi_ssid, settings.wifi_password)

    time_module.set_ntp_time()

    ha_client = HaMqttPublisher(settings.mqtt_broker)

    ha_client.publish_config()

    controllers = []
    webserver = Webserver(controllers)

    tsf = asyncio.Event()  # type: ignore

    task = asyncio.create_task(webserver.run(tsf))

    while True:
        await asyncio.sleep(300)  # type: ignore
        temperature_module.log_temperature()
        await asyncio.sleep(0)
        temperature = temperature_module.get_temperature()
        ha_client.publish_temperature(temperature)
        await asyncio.sleep(0)
        led_module.led_toggle()

asyncio.run(main())
