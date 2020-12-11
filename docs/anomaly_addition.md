 Python script for anomaly detection:
A python code for generating random values and detecting the ones that are irrelevant / falls out of the required range set has been written. In built python functions were used to implement the same.
MQTT broker:
 MQTT broker was set up to establish the connection. The pub sub server was set up and anomaly was published.
Influx and Grafana:
The anomaly data was stored into the Influx database. And the data was depicted using Grafana as interface.

Code

```
import requests
import time
import paho.mqtt.client as mqtt
import json
from pprint import pprint
def weather_data(query):
    res=requests.get('http://api.openweathermap.org/data/2.5/weather?'+query+'&APPID=b35975e18dc93725acb092f7272cc6b8&units=metric');
    return res.json()
def print_weather(result,city):
    client1=mqtt.Client("weather")
    client1.connect("192.168.1.6")
    temperature=result['main']['temp']
    #print(type(temperature))
    client1.publish("temp_sensor",json.dumps({"name":"tempreading","city":city,"value":result['main']['temp']}),qos=0)
    print("{}'s temperature: {}°C ".format(city,result['main']['temp']))
 
def main():
    city=input('Enter the city:')
    i=1
    print()
    while True:
        query='q='+city
        try:
            w_data=weather_data(query)
        except requests.exceptions.RequestException as e:
            print(i)
            print("Connection lost")
            i=i+1
            time.sleep(5)
            continue
        print(i)
        print_weather(w_data, city)
        i=i+1
        time.sleep(5)

   
name="main"

if name=='main':
    main()
```
