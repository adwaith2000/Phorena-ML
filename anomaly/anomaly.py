import numpy as np
import matplotlib.pyplot as plt
from celluloid import Camera
from collections import defaultdict
from functools import partial
from tqdm import tqdm
from influxdb import InfluxDBClient
import random
from tsmoothie.smoother import *
import pprint

def find_anomalies():
    client = InfluxDBClient(host='10.152.183.211', port=8086, username='exofense', password='password')
    client.switch_database('exofense')

    result = client.query('SELECT * FROM "exofense"."autogen"."temp_reading"')
    points = list(result.get_points())

    data = []
    data.append(list(map(lambda pt: pt['value'], points)))

    total = 0

    for i in range(0, len(data[0])-5, 5):
        if i > 20: 
            total += 1
            print(i, data[0][i], data[0][i+1], data[0][i-1])

    print(total)

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


    ### GENERATE DATA ###

    np.random.seed(42)
    n_series, timesteps = 1, len(data[0])

    # data = np.array([[1]*200, [1]*200, [28 if i == 20 else 35 for i in range(200)]])
    data = np.array(data)

    plt.plot(data.T)
    np.set_printoptions(False)

    false_positive, false_negative = 0, 0


    ### SLIDING WINDOW PARAMETER ###

    window_len = 20

    ### SIMULATE PROCESS REAL-TIME AND CREATE GIF ###

    fig = plt.figure(figsize=(18,10))
    camera = Camera(fig)

    anomalies = []
    axes = [plt.subplot(n_series,1,ax+1) for ax in range(n_series)]
    series = defaultdict(partial(np.ndarray, shape=(n_series,1), dtype='float32'))


    for i in range(timesteps):

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

                if(data[0][i-2] - data[0][i-1] < 0.5):
                    false_negative += 1
                    print(f'False neagtive: {i} {data[0][i]} {data[0][i-1]}')

                else:
                    print(f'Positive: {i} {data[0][i-2]} {data[0][i-1]} {data[0][i]}')
                    points[i-1]["anomaly"] = "true"
                    print(i)

            elif(abs(data[0][i]-data[0][i-1]) > 0.5):
                false_positive += 1
                print(f'Positives: {i} {data[0][i-2]} {data[0][i-1]} {data[0][i]}')
                points[i]["anomaly"] = "true"


            for s in range(n_series):
                pltargs = {k:v[s,:] for k,v in series.items()}
                plot(axes[s], i, is_anomaly[s], window_len, 
                             **pltargs)

        if i>=timesteps:
            continue

        series['original'] = np.hstack([series['original'], data[:,[i]]])


    return points
