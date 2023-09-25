import utime, rp2
from machine import Pin

@rp2.asm_pio(set_init=rp2.PIO.OUT_LOW)
def blink():
    wrap_target()
    set(pins, 1)
    nop()
    nop()
    nop()
    set(pins, 0)
    nop()
    nop()
    nop()
    nop()
    wrap()

sm = rp2.StateMachine(0, blink, freq=2000, set_base=Pin(25))

sm.active(1)
utime.sleep(10)
sm.active(0)