from mqtt.mqtt_module import HaMqttPublisher
from temperature.temperature_provider import TemperatureProvider
import asyncio


class AsyncTemperatureHAPublisher():
    mqtt_broker: str
    task: asyncio.Task
    tmp_provider: TemperatureProvider
    publish_interval: int

    def __init__(self, mqtt_broker: str,
                 tsf: asyncio.Event,
                 tmp_provider: TemperatureProvider,
                 publish_interval: int = 10) -> None:

        self.mqtt_broker = mqtt_broker
        self.tmp_provider = tmp_provider
        self.publish_interval = publish_interval
        self.task = asyncio.create_task(self.run(tsf))

    async def run(self, tsf: asyncio.Event):
        ha_client = HaMqttPublisher(self.mqtt_broker)

        ha_client.publish_config()

        await asyncio.sleep(0)

        while not tsf.is_set():
            temperature = await self.tmp_provider.get_temperature()
            ha_client.publish_temperature(temperature)
            await asyncio.sleep(self.publish_interval)