import utils.settings_module as settings_module
from utils.json_serializer import JsonSerializer
from webserver.ControllerFactory import Controller, ControllerFactory


class SettingsController(Controller):
    def get(self):
        print("SettingsController.get")

        settings = settings_module.load_settings()
        return settings


class SettingsControllerFactory(ControllerFactory):
    def __init__(self) -> None:
        super().__init__()
        self.controller_path = "settings"

    def create_controller(self) -> Controller:
        return SettingsController()


if __name__ == '__main__':
    settings_controller = SettingsController()

    print(settings_controller.get())
