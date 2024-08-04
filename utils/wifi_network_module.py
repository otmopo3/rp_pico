import network
import ubinascii
import urequests
import time
import utils.led_module as led_module

wlan = network.WLAN(network.STA_IF)


def connect_wifi(wlan_ssid, password, max_attempts=-1, uri_to_test='', status_check_timeout=1):
    log_wlan_info()

    # Disable power-save mode
    wlan.config(pm=network.WLAN.PM_PERFORMANCE)  # type: ignore

    wlan.active(True)

    time.sleep(1)
    if (not wlan.active()):
        wlan.active(True)

    connected: bool = False
    while not connected:
        wlan.connect(wlan_ssid, password)
        print("wlan.connect")
        wait_connection(max_attempts, status_check_timeout)
        connected = handle_connection_result(uri_to_test)
        if not connected:
            time.sleep(status_check_timeout)


def handle_connection_result(uri_to_test) -> bool:
    if wlan.status() >= network.STAT_GOT_IP:
        print("Connected")
        client_ip, subnet, gateway, DNS = wlan.ifconfig()
        print(
            f'ip = {client_ip}, subnet = {subnet}, gateway = {gateway}, DNS = {DNS}')
        print(f"hostname = {network.hostname()}")
        if (uri_to_test != ''):
            try:
                print(f'Trying to connect to {uri_to_test}')
                r = urequests.get(uri_to_test)
                print(r.content)
                r.close()
            except Exception as exception:
                print(f'Error connecting to test url: {exception}')
                return False

        return True
    else:
        print(
            f'!!!Connection failed!!! wlan_status= {str(wlan.status())} Going to reconnect in few seconds')

    return False


def wait_connection(max_attempts, status_check_timeout):
    while max_attempts != 0:
        if wlan.status() >= network.STAT_GOT_IP:
            break

        if wlan.status() < network.STAT_IDLE:
            break

        if max_attempts > 0:
            max_attempts -= 1

        led_module.led_toggle()
        print('waiting for connection...' +
              ' wlan_status=' + str(wlan.status()))
        time.sleep(status_check_timeout)


def get_ip():
    return wlan.ifconfig()[0]


def log_wlan_info():
    mac_part = wlan.config('mac')

    mac = ubinascii.hexlify(mac_part, ':').decode()  # type: ignore
    print('mac=' + mac)
    print("Connecting to wi-fi")


if __name__ == '__main__':
    import utils.settings_module as settings_module
    settings = settings_module.load_settings()
    connect_wifi(settings.wifi_ssid, settings.wifi_password,
                 uri_to_test="https://wiby.me/")
