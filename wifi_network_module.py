import network
import ubinascii
import urequests
import time
import led_module

wlan = network.WLAN(network.STA_IF)

def connect_wifi(wlan_ssid, password, max_attempts=-1, uri_to_test='', status_check_timeout=1):    
    log_wlan_info()
    
    wlan.connect(wlan_ssid, password)   
    
    wait_connection(max_attempts, status_check_timeout)
    handle_connection_result(uri_to_test)    
    
def handle_connection_result(uri_to_test):
    if wlan.status() >= 3:
        print("Connected")
        status = wlan.ifconfig()
        print('ip = ' + status[0])
        if (uri_to_test != ''):
            r = urequests.get(uri_to_test)
            print(r.content)
            r.close()   
    else:
        print("!!!Connection failed!!!")
        
    print('wlan_status=' + str(wlan.status()))
    
def log_wlan_info():
    print('wlan_status=' + str(wlan.status()))
    wlan.active(True)
    print('wlan_status=' + str(wlan.status()))
    mac = ubinascii.hexlify(network.WLAN().config('mac'),':').decode()
    print('mac=' + mac)
    print("Connecting to wi-fi")

def wait_connection(max_attempts, status_check_timeout):
    while max_attempts != 0:
        if wlan.status() >= 3:
            break
        
        if max_attempts > 0:
            max_attempts -= 1
        
        led_module.led_toggle()
        print('waiting for connection...' + ' wlan_status=' + str(wlan.status()))
        time.sleep(status_check_timeout)

def get_ip():
    return wlan.ifconfig()[0]
    
if __name__ == '__main__':
    connect_wifi(uri_to_test='')

