from machine import Pin
import asyncio

class LED_async():
    def __init__(self, led_no):
        print(f"start init pin={led_no}")
        self.led = Pin(led_no, Pin.OUT)
        self.delay_ms = 200
        self.task = asyncio.create_task(self.run())
        print("end init")

    async def run(self):
        print("run")
        while True:
            self.led.toggle()
            await asyncio.sleep_ms(self.delay_ms)
            print("toggle")

    def flash(self, delay_ms):
        self.delay_ms = delay_ms

    def on(self):
        self.led.on()
        self.rate = 0

    def off(self):
        self.led.off()
        self.rate = 0

async def test():
    async_led = LED_async("LED")
    async_led.flash(2000)
    while True:
        await asyncio.sleep_ms(100)

async def test_while_button():
    async_led = LED_async("LED")
    async_led.flash(2000)
    button = ButtonCounter(0)

    while button.cnt < 1:
        await asyncio.sleep_ms(100)

if __name__ == '__main__':
    asyncio.run(test_while_button())
    
class ButtonCounter():
    def __init__(self, button_pin):
        print(f"start button init pin={button_pin}")
        self.button = machine.Pin(0, machine.Pin.IN, machine.Pin.PULL_DOWN)
        self.button.irq(self.on_button_click) # type: ignore
        self.cnt = 0
        
    def on_button_click(self, pin):
        print(f"{pin.value()} {self.cnt}" )
        self.cnt += 1
        print(self.cnt)   