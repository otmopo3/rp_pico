import utime, machine
from machine import Pin

import wifi_network_module
import time_module
import led_module
import temperature_module
import mqtt_module
import settings_module

from mqtt_module import HaMqttPublisher

settings = settings_module.load_settings()

wifi_network_module.connect_wifi(settings.wifi_ssid, settings.wifi_password)

time_module.set_ntp_time()

led_module.led_on()

ha_client = HaMqttPublisher(settings.mqtt_broker)

ha_client.publish_config()

while True:
    temperature_module.log_temperature()
    temperature = temperature_module.get_temperature()
    ha_client.publish_temperature(temperature)
    utime.sleep(300)
    led_module.led_toggle()
