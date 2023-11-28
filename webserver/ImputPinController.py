
from utils.json_serializer import JsonSerializer
from webserver.ControllerFactory import ControllerFactory
from webserver.ControllerFactory import Controller

class PinState:
    pin_num: int
    pin_value: int

class InputPinControler(Controller):
    def get(self):
        print("InputPinControler.get")
        
        state = PinState()
        state.pin_num = 0
        state.pin_value = 1

        return state
        
class InputPinControlerFactory(ControllerFactory):
    controller_path = "input_pin_value"
    
    def create_controller(self) -> Controller:
        return InputPinControler()
    