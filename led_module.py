import utime
from machine import Pin

led_onboard = Pin("LED", Pin.OUT)

def led_toggle():    
    led_onboard.toggle()
    
def led_on():    
    led_onboard.on()

def led_off():    
    led_onboard.off()

