import utime
from temperature.temperature_provider import TemperatureProvider


import asyncio


class TemperatureLogger():
    tmp_provider: TemperatureProvider
    log_interval: int
    task: asyncio.Task

    def __init__(self,
                 tmp_provider: TemperatureProvider,
                 tsf: asyncio.Event,
                 log_interval: int = 10):

        self.task = asyncio.create_task(self.run(tsf))
        self.tmp_provider = tmp_provider
        self.log_interval = log_interval
        self.file = open("temps.txt", "a")

    async def run(self, tsf: asyncio.Event):
        while not tsf.is_set():
            temperature = await self.tmp_provider.get_temperature()
            log_temp_str = str(utime.localtime()) + " " + \
                str(temperature) + "\n"
            self.file.write(log_temp_str)
            self.file.flush()
            print(f'Writen temp to file: {log_temp_str}')
            await asyncio.sleep(self.log_interval)
