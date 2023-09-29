import machine
import asyncio
from asyncio import Event

button = machine.Pin(0, machine.Pin.IN, machine.Pin.PULL_DOWN)
cnt = 1
event = Event()
tsf = asyncio.ThreadSafeFlag() # type: ignore


def on_button_click(pin):
    global event

    if (pin.value() == 1):
        tsf.set()
    # sys.exit()
    # machine.reset()


async def waiter(tsf):
    while True:
        print('Waiting for event')
        await tsf.wait()  # Pause here until event is set
        print('Waiter got event.')
        tsf.clear()  # Flag caller and enable re-use of the event


button.irq(on_button_click)  # type: ignore


async def main():

    task = asyncio.create_task(waiter(tsf))
    while True:
        await asyncio.sleep(10)
        print("looping")


asyncio.run(main())
