from json_serializer import JsonSerializer


class Settings:
    wifi_ssid: string
    wifi_password: string

    mqtt_broker: string


def load_settings(filename='settings.json'):
    f = open(filename)
    settings_str = f.read()
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
    import wifi_network_module
    settings = settings_module.load_settings()
    print(settings.wifi_ssid)
