import dht
import machine


d = dht.DHT22(machine.Pin(1))

d.measure()
d.temperature()
d.humidity()