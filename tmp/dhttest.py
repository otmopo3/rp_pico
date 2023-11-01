import dht
import machine


d = dht.DHT11(machine.Pin(0))

d.measure()
print(d.temperature())
print(d.humidity())