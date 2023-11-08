from webserver.ControllerFactory import Controller, ControllerFactory


class RandomController(Controller):

    def __init__(self) -> None:
        super().__init__()

    def get(self):
        print("SettingsController2.get")
        return "234234"
    
class RandomControllerFactory2(ControllerFactory):
    def __init__(self) -> None:
        super().__init__()
        self.controller_path = "some_other_path"

    def create_controller(self) -> Controller:
        return RandomController()