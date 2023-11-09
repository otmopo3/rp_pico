from utils.json_serializer import JsonSerializer


class Settings:
    wifi_ssid: str
    wifi_password: str

    mqtt_broker: str

    file_log_interval: int
    ha_publish_interval: int

    temperature_measure_interval: int
    dht11_pin: int

    webserver_port: int
    webserver_web_folder: str
    webserver_api_prefix: str


def load_settings(filename='settings.json') -> Settings:
    f = open(filename)
    settings_str = f.read()
    print(f"Loaded settings: {settings_str}")
    json_helper = JsonSerializer(Settings())
    loaded_settings = json_helper.Deserialize(settings_str)
    return loaded_settings


def save_settings(settings, filename='settings.json'):
    json_helper = JsonSerializer(settings)
    json_str = json_helper.Serialize()
    f = open(filename, 'w')
    f.write(json_str)
    f.close()


if __name__ == '__main__':
    import settings_module
    settings = settings_module.load_settings()
    print(settings.wifi_ssid)
