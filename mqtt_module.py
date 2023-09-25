from umqttsimple import MQTTClient
import machine
import utime

import device_module
import wifi_network_module

class MqttPublisher:
    def __init__(self, server_address, topic):
        client_id = 'rp2 pico'
        self.mqtt_client = MQTTClient(client_id, server_address)
        self.topic = topic
        
    def connect(self):        
        self.mqtt_client.connect()
        
    def disconnect(self):
        self.mqtt_client.disconnect()
        
    def publish(self, msg):
        self.mqtt_client.publish(self.topic, msg)

class HaMqttPublisher:
    
    def __init__(self, server_address):
        self.dev_id = device_module.get_device_id()
        self.base_topic = 'homeassistant/sensor/sensorRp2Pico3' + self.dev_id
        self.state_topic = self.base_topic+'/state'
        self.server_address = server_address
        
     
    def publish_config(self):
        try:
            config_topic = self.base_topic + '/config'
            mqtt_publisher = MqttPublisher(self.server_address, config_topic)
            mqtt_publisher.connect()                
           
            config_str='{"device_class": "temperature", "state_topic": "' + self.state_topic + '",'
            config_str=config_str+' "unit_of_measurement": "°C", "value_template": "{{ value_json.temperature}}",'
            config_str=config_str+'"unique_id": "'+self.dev_id+'", "device": {"identifiers": ["rp2pico"], "name": "rp2pico" }} }'
            
            mqtt_publisher.publish(config_str)
            
            mqtt_publisher.disconnect()
            
            print('pusblished Home Assistant Mqtt config')
        except:
            print('Error pusblishing Home Assistant Mqtt config')
        
         
    def publish_temperature(self, temperature):
        try:
            temp_str=str(temperature)
            
            mqtt_publisher = MqttPublisher(self.server_address, self.state_topic)
            mqtt_publisher.connect()  

            temperature_json = '{ "temperature": ' + temp_str + ' }'
            mqtt_publisher.publish(temperature_json)
            
            mqtt_publisher.disconnect()
            
            print('Pusblished Home Assistant Mqtt temperature')
        except:
             print('Error pusblishing Home Assistant Mqtt temperature')
            

if __name__ == '__main__':
    pass
    client = HaMqttPublisher()
    
    client.publish_config()

    utime.sleep(1)
    
    client.publish_temperature(19.7)  