from AsyncTemperatureHAPublisher import AsyncTemperatureHAPublisher
from temperature.TemperatureLogger import TemperatureLogger
from temperature.temperature_provider import AsyncDht11TemperatureProvider, InternalTemperatureProvider
import wifi_network_module
import time_module
import led_module
import settings_module
import asyncio
from webserver.webserver_module import Webserver


async def main():
    settings: settings_module.Settings = settings_module.load_settings()

    wifi_network_module.connect_wifi(
        settings.wifi_ssid, settings.wifi_password)

    time_module.set_ntp_time()

    webserver = Webserver(api_prefix=settings.webserver_api_prefix,
                          web_folder=settings.webserver_web_folder,
                          port=settings.webserver_port)

    tsf = asyncio.Event()  # type: ignore

    task = asyncio.create_task(webserver.run(tsf))

    # tmp_provider = InternalTemperatureProvider()
    tmp_provider = AsyncDht11TemperatureProvider(
        pin_index=settings.dht11_pin,
        measure_interval=settings.temperature_measure_interval)

    ha_publisher = AsyncTemperatureHAPublisher(
        settings.mqtt_broker, tsf, tmp_provider,
        publish_interval=settings.ha_publish_interval)

    tmp_logger = TemperatureLogger(
        tmp_provider, tsf,
        log_interval=settings.file_log_interval)

    while True:
        await asyncio.sleep(300)  # type: ignore
        led_module.led_toggle()

asyncio.run(main())
