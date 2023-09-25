import machine, utime

sensor_temp = machine.ADC(4)
conversion_factor = 3.3/ (65535)
file = open("temps.txt", "a")

def get_temperature():
    raw_value = sensor_temp.read_u16()        
    voltage = raw_value * conversion_factor    
    # The temperature sensor measures the Vbe voltage of a biased bipolar diode, connected to
    #the fifth ADC channel
    # Typically, Vbe = 0.706V at 27 degrees C, with a slope of -1.721mV (0.001721) per degree.
    temperature = 27 - (voltage - 0.706)/0.001721    
    return temperature    

def log_temperature():
    temperature = get_temperature()
    log_temp_str = str(utime.localtime()) + " " + str(temperature) + "\n"
    file.write(log_temp_str)
    file.flush()
    print(f'Writen temp to file: {log_temp_str}')

def log_tempeature_loop():
    while True:
        log_temperature()
        utime.sleep(15)

if __name__ == '__main__':
    log_tempeature_loop()


