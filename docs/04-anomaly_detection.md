## Using tsmoothie
Documentation for [anomaly.py](../anomaly/anomaly.py)

### Step 1: Importing the libraries
We use celluloid library to generate the gif of our anomaly detection program,
tqdm to show progress bar and tsmoothie to detect anomalies 
```py
import numpy as np
import matplotlib.pyplot as plt
from celluloid import Camera
from collections import defaultdict
from functools import partial
from tqdm import tqdm
from influxdb import InfluxDBClient
import random
import pprint
from tsmoothie.smoother import *
```

### Step 2: Fetching data from the database
The following code fetches the temperature readings recorded in the
InfluxDB
```py
client = InfluxDBClient(host='YOUR_HOST_NAME', port=8086, username='YOUR_USERNAME', password='YOUR_PASSWORD')
client.switch_database('exofense')

result = client.query('SELECT * FROM "exofense"."autogen"."temp_reading"')
points = result.get_points()
pprint.pprint(list(points)[:3])
```
The output will be like:
```
    [{'host': 'telegraf-794bc96857-h5bkt',
  'sensor_name': None,
  'time': '2020-11-13T14:25:19.492971Z',
  'topic': 'temperature',
  'value': 30.0},
 {'host': 'telegraf-794bc96857-h5bkt',
  'sensor_name': None,
  'time': '2020-11-13T14:26:19.805314Z',
  'topic': 'temperature',
  'value': 30.0},
 {'host': 'telegraf-794bc96857-h5bkt',
  'sensor_name': None,
  'time': '2020-11-13T14:27:20.574169Z',
  'topic': 'temperature',
  'value': 30.0}]
```

As we are only interested in the temperature readings we can append
those readings to a list by
```py
data = []
data.append(list(map(lambda pt: pt['value'], list(points))))
```

### Step 3: Introducing some anomaly
```py
total = 0

for i in range(0, len(data[0])-5, 5):
    if i > 20: 
        total += 1
        data[0].insert(i, random.randint(80, 90))
        print(i, data[0][i], data[0][i+1], data[0][i-1])
```
Here we generate random values and insert it to the data[0] array at multiples of 5.


### Step 4: Utility function to plot the data
```py
def plot(
    ax,
    i,
    is_anomaly,
    window_len,
    color='blue',
    **pltargs
):
    posrange = np.arange(0, i)
    ax.fill_between(
        posrange[window_len],
        pltargs['low'][1:],
        pltargs['up'][1:],
        color=color,
        linewidth=3
    )

    c = 'red' if is_anomaly else 'black'
    ax.scatter(i-1, pltargs['original'][-1], c=c)
    ax.scatter(i-1, pltargs['smooth'][-1], c=color)

    ax.plot(posrange, pltargs['original'][1:], '.k')
    ax.plot(
        posrange[window_len:], 
        pltargs['smooth'][1:], 
        color=color, 
        linewidth=3
    )

    if 'ano_id' in pltargs.keys() and pltargs['ano_id'].sum() > 0:
        not_zeros = pltargs['ano_id'][pltargs['ano_id'] != 0] - 1
        ax.scatter(
            not_zeros, 
            pltargs['original'][1:][not_zeros], 
            c='red', 
            alpha=1.
        )
```
This function will be plot smoothened curve in color that we pass to the function (default is blue) with anomalies in red color and non anomalous data in black color

### Step 5: Setting up parameters
```py
n_series, timesteps = 1, len(data[0])

data = np.array(data)

plt.plot(data.T)
np.set_printoptions(False)

false_positive, false_negative = 0, 0

window_len = 20 # Sliding window parameter

fig = plt.figure(figsize=(18,10))
camera = Camera(fig)

anomalies = []
axes = [plt.subplot(n_series,1,ax+1) for ax in range(n_series)]
series = defaultdict(partial(np.ndarray, shape=(n_series,1), dtype='float32'))
```

Here n_series is the number of series we are detecting anomaly on. Since we use only temperature_reading in this example we set that to 1.

### Step 6: Detecting Anomalies
```py

for i in tqdm(range(timesteps+1), total=(timesteps+1)):
    
    if i>window_len:
    
        smoother = ConvolutionSmoother(window_len=window_len, window_type='ones')
        smoother.smooth(series['original'][:,-window_len:])

        series['smooth'] = np.hstack([series['smooth'], smoother.smooth_data[:,[-1]]]) 

        _low, _up = smoother.get_intervals('sigma_interval', n_sigma=2)
        series['low'] = np.hstack([series['low'], _low[:,[-1]]])
        series['up'] = np.hstack([series['up'], _up[:,[-1]]])

        is_anomaly = np.logical_or(
            series['original'][:,-1] > series['up'][:,-1], 
            series['original'][:,-1] < series['low'][:,-1]
        ).reshape(-1,1)
        
        if is_anomaly.any():
            series['ano_id'] = np.hstack([series['ano_id'], is_anomaly*i]).astype(int)
        
        if(is_anomaly[0][0]):
            anomalies.append(i)
            if(i % 5 != 1):
                false_negative += 1

        elif(i % 5 == 1 and abs(data[0][i]-data[0][i-1]) > 5):
            print(data[0][i])
            false_positive += 1
            
        for s in range(n_series):
            pltargs = {k:v[s,:] for k,v in series.items()}
            plot(axes[s], i, is_anomaly[s], window_len, 
                         **pltargs)

        camera.snap()
        
    if i>=timesteps:
        continue
    
    series['original'] = np.hstack([series['original'], data[:,[i]]])
```

We use tsmoothie's ConvolutionSmoother to smooth the data and get an low and up value for each data point. If the data point lies between this up and low it is not labelled as anomaly. We use numpy hstack to stack multiple series into a single object and perform vectorised operations on it.

### Step 7: Printing results
```py
print(anomalies)
print(false_positive, total)
print(false_positive/total)
print(false_negative)
    
print('CREATING GIF...')  # it may take a few seconds
camera._photos = [camera._photos[-1]] + camera._photos
animation = camera.animate()
animation.save('animation1.gif')
plt.close(fig)
print('DONE')
```
![](../animation1.gif)