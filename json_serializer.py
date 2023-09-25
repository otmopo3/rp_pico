import json

class JsonSerializer:
    def __init__(self, object):
        self.object = object
        
    def Serialize(self):
        json_str = json.dumps(self.object.__dict__)
        return json_str
    
    def Deserialize(self, json_str):
        loaded_dict = json.loads(json_str)
        obj_type = type(self.object)
        loaded_settings = type(obj_type.__qualname__,(),loaded_dict)
        return loaded_settings