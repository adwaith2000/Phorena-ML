# A sensor simulation that generates a random number every
# 30 seconds and publish it to the mqtt server


"""

JSON Format

{
	"name": "temperature",
	"sensor_name": "room_temp_sensor"
	"value": 77
}

"""

import random
import os
import sys
import datetime
import time
import socket
import json
import paho.mqtt.client as paho

class TemperatureSensor:
	"""
	Periodically sends message to MQTT
	"""

	TOPIC_NAME = "temperature"
	SENSOR_NAME = "room_temp_sensor"
	MEASUREMENT_NAME = "temperature"
	BROKER = "10.152.183.49" # Use your mosquitto service local IP
	PORT = 1883
	
	def __init__(self):
		# Initial setup
		try:
			ts = datetime.datetime.now().isoformat()
			client_id = f'client-{ts[-6:]}'
			
			self.client = paho.Client(client_id)
			self.client.connect(self.BROKER, self.PORT)
			print("Connection established")

		except Exception as e:
			print("Connection failed")
			print(e)

	def read_value(self):
		"""
		Returns a random value for temperature
		"""
		return random.uniform(68.0, 77.0)

	def send_to_server(self, reading: int = 0.0):
		"""
		Sends the message to server
		"""
		self.client.publish(self.TOPIC_NAME, json.dumps({
			"name": self.MEASUREMENT_NAME,
			"sensor_name": self.SENSOR_NAME,
			"value": reading
		}), qos = 0)
		print("Message published")

	def start(self):
		"""
		Reads a value and sends it to broker in every 30s
		"""
		while True:
			value = self.read_value()
			self.send_to_server(value)
			time.sleep(30)


if __name__ == '__main__':
	temperature_sensor = TemperatureSensor()
	temperature_sensor.start()