import datetime
import requests
import json
import time
import paho.mqtt.client as paho
from sensor import Sensor

class TempHumiditySensor(Sensor):
    CITY_NAME = "mumbai"
    topic_name = "temperature"

    def __init__(self):
        ts = datetime.datetime.now().isoformat()
        self.sensor_name = f'client-{ts[-6:]}'

        try:
            self.client = paho.Client(self.sensor_name)
            self.client.connect(self.BROKER, self.PORT)
            print(f"{self.sensor_name}: Established connection")
        
        except Exception as e:
            print(f"{self.sensor_name}: Failed connection")
            print(e)

    def read_value(self):
        response = requests.get(
                f'http://api.openweathermap.org/data/2.5/weather?&q={self.CITY_NAME}&APPID=b35975e18dc93725acb092f7272cc6b8&units=metric',
                timeout=8
            ).json()
        return response['main']['temp'], response['main']['humidity']
    
    def start(self):
        while True:
            value = self.read_value()
            self.send_cpu_data_to_server()
            self.client.publish(self.topic_name, json.dumps({
                "name": "temp_reading",
                "sensor_name": self.sensor_name,
                "value": value[0]
            }))
            self.client.publish(self.topic_name, json.dumps({
                "name": "humidity_reading",
                "sensor_name": self.sensor_name,
                "value": value[1]
            }))
            print(f"{self.sensor_name}: Published data {value}")
            time.sleep(60)


if __name__ == '__main__':
    sensor = TempHumiditySensor()
    sensor.start()