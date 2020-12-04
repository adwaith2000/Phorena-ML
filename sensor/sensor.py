import psutil
from abc import ABC, abstractmethod, abstractproperty
import json

class Sensor(ABC):
    # Use the cluster IP of mosquitto until the app is deployed to the cluster
    BROKER = "10.152.183.49"
    PORT = 1883

    @abstractmethod
    def read_value(self):
        raise NotImplementedError

    def read_cpu_data(self):
        """
        Returns a tuple of cpu usage and physical mem usage
        """
        return psutil.cpu_percent(interval = 1), psutil.virtual_memory().percent
    
    def send_cpu_data_to_server(self):
        (cpu_usage, mem_usage) = self.read_cpu_data()
        self.client.publish(self.topic_name, json.dumps({
            "name": "cpu_reading",
            "sensor_name": self.sensor_name,
            "value": cpu_usage
        }))
        self.client.publish(self.topic_name, json.dumps({
            "name": "mem_reading",
            "sensor_name": self.sensor_name,
            "value": mem_usage
        }))

    @abstractmethod
    def start(self):
        raise NotImplementedError

