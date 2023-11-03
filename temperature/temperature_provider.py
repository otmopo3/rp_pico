import asyncio
import machine
import dht
import time


class TemperatureProvider():
    def __init__(self) -> None:
        pass

    async def get_temperature(self) -> int:
        await asyncio.sleep(0)
        return 0


class InternalTemperatureProvider(TemperatureProvider):
    conversion_factor = 3.3 / (65535)
    sensor_temp: machine.ADC

    def __init__(self) -> None:
        super().__init__()
        self.sensor_temp = machine.ADC(4)

    async def get_temperature(self):
        raw_value = self.sensor_temp.read_u16()
        await asyncio.sleep(0)
        voltage = raw_value * self.conversion_factor
        # The temperature sensor measures the Vbe voltage of a biased bipolar diode, connected to
        # the fifth ADC channel
        # Typically, Vbe = 0.706V at 27 degrees C, with a slope of -1.721mV (0.001721) per degree.
        temperature = 27 - (voltage - 0.706)/0.001721
        return temperature


class AsyncDht11TemperatureProvider(TemperatureProvider):
    sensor: dht.DHT11
    measure_interval_ms: int
    last_measure: int = 0
    lock: asyncio.Lock = asyncio.Lock()

    def __init__(self, pin_index: int, measure_interval=300) -> None:
        super().__init__()
        self.sensor = dht.DHT11(machine.Pin(pin_index))
        self.measure_interval_ms = measure_interval * 1000

    async def get_temperature(self) -> int:
        await self.measure_if_need()
        return self.sensor.temperature()

    async def measure_if_need(self) -> None:
        sensor = self.sensor
        await self.lock.acquire()
        ticks_ms_now = time.ticks_ms()
        last_measure_diff_ms = time.ticks_diff(ticks_ms_now, self.last_measure)
        if (self.last_measure > 0 and last_measure_diff_ms < self.measure_interval_ms):
            return

        try:
            sensor.measure()
            self.last_measure = ticks_ms_now
            print(f"AsyncDht11TemperatureProvider: measure temperature")
        except Exception as ex:
            print(
                f"AsyncDht11TemperatureProvider: Error measuring temprature on sensor{sensor.pin} {ex}:")

        self.lock.release()
        await asyncio.sleep(0)


async def main():
    provider = AsyncDht11TemperatureProvider(0)
    temp = await provider.get_temperature()
    print(temp)


if __name__ == '__main__':
    asyncio.run(main())
