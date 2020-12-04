import numpy as np
import matplotlib.pyplot as plt
from celluloid import Camera
from collections import defaultdict
from functools import partial
from tqdm import tqdm
from influxdb import InfluxDBClient

from tsmoothie.smoother import *

client = InfluxDBClient(host='10.152.183.211', port=8086, username='exofense', password='password')
client.switch_database('exofense')

temp_result = client.query('SELECT * FROM "exofense"."autogen"."temp_reading" LIMIT 90')
temp_points = temp_result.get_points()
humidity_result = client.query('SELECT * FROM "exofense"."autogen"."humidity_reading"')
humidity_points = humidity_result.get_points()

data = []
# data.append(list(map(list(points), lambda pt: pt['value'])))
data.append(list(map(lambda pt: pt['value'], list(temp_points))))
data[0][60] = 30
data.append(list(map(lambda pt: pt['value'], list(humidity_points))))
    

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
    ax.scatter(i-1, pltargs['smooth'][-1], c=color)
    ax.scatter(i-1, pltargs['original'][-1], c=c)

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


### GENERATE DATA ###

np.random.seed(42)

n_series, timesteps = 2, len(data[0])

data = np.array([data[0], data[1]])

plt.plot(data.T)
np.set_printoptions(False)


### SLIDING WINDOW PARAMETER ###

window_len = 20

### SIMULATE PROCESS REAL-TIME AND CREATE GIF ###

fig = plt.figure(figsize=(18,10))
camera = Camera(fig)

axes = [plt.subplot(n_series,1,ax+1) for ax in range(n_series)]
series = defaultdict(partial(np.ndarray, shape=(n_series,1), dtype='float32'))


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
            
        for s in range(n_series):
            pltargs = {k:v[s,:] for k,v in series.items()}
            plot(axes[s], i, is_anomaly[s], window_len, 
                         **pltargs)

        camera.snap()
        
    if i>=timesteps:
        continue
    
    series['original'] = np.hstack([series['original'], data[:,[i]]])

    
print('CREATING GIF...')  # it may take a few seconds
camera._photos = [camera._photos[-1]] + camera._photos
animation = camera.animate()
animation.save('animation2.gif')
plt.close(fig)
print('DONE')