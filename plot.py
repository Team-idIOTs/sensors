import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as signal#Import signal processing module
import scipy
# Read your data
from config import *
import pyrebase
import os

def make_np_array(filename):
    with open(filename) as f:
        data = f.readlines()
        data = np.asarray([x[:-1].split(",") for x in data])
        return data

def filter(data):
    data = data[:, 4].astype(float)
    b, a = signal.butter(N=1, Wn=0.05) # 1st order with cutoff freq of 5Hz
    return signal.filtfilt(b, a, data, padlen=150)

def plot(data):
    accelx = data[:,0].astype(float)
    accely = data[:,1].astype(float)
    accelz = data[:,2].astype(float)

    gyrox = data[:,3].astype(float)
    gyroy = data[:,4].astype(float)
    gyroy = data[:,5].astype(float)

    b, a = signal.butter(N=1, Wn=0.05) # 1st order with cutoff freq of 5Hz
    accelx = signal.filtfilt(b, a, accelx, padlen=150)
    accely = signal.filtfilt(b, a, accely, padlen=150)
    accelz = signal.filtfilt(b, a, accelz, padlen=150)

    gyrox = signal.filtfilt(b, a, gyrox, padlen=150)
    gyroy = signal.filtfilt(b, a, gyroy, padlen=150)
    #gyroz = signal.filtfilt(b, a, gyroz, padlen=150)

    #b, a = signal.butter(N=1, Wn=0.00001) # 1st order with cutoff freq of 5Hz
    #gyrox = signal.filtfilt(b, a, gyrox, padlen=150)
    gyroy = signal.filtfilt(b, a, gyroy, padlen=150)
    #gyroz = signal.filtfilt(b, a, gyroz, padlen=150)



    plt.plot(gyroy)
    zcross = np.where(np.diff(np.sign(gyroy)))[0]
    start_points = []
    end_points = []
    for z in range(len(zcross) - 2):
        segment = gyroy[zcross[z]:zcross[z+1]]
        nextsegment = gyroy[zcross[z+1]:zcross[z+2]]
        if ((np.max(segment) > 9) and (np.min(nextsegment) < -9)):
            start_points.append(zcross[z])
            end_points.append(zcross[z+2])
    plt.plot(start_points, gyroy[start_points], 'go')
    plt.plot(end_points, gyroy[start_points], 'ro')

    D = 28
    length = []
    for i in range(len(start_points)):
        stride = gyroy[start_points[i]:end_points[i]]
        t_end = len(stride)-1
        a_x = -accelx[start_points[i]:end_points[i]]
        a_y = accely[start_points[i]:end_points[i]]
        theta = np.cumsum(stride)
        a_hor = np.cos(theta)*a_y - np.sin(theta)*a_x
        v_hor_gyr = np.cos(theta)*-stride*D
        v_hor = np.cumsum(a_hor) + v_hor_gyr
        correction = (v_hor_gyr[t_end] - v_hor[t_end])/len(stride)
        v_hor_corrected = v_hor + correction*range(len(stride))
        length.append(np.trapz(v_hor_corrected))
    print(length)


    plt.show()

firebase = pyrebase.initialize_app(config)
storage = firebase.storage()

file_name = "data20sec"
#storage.child(file_name).download(file_name)
bigsteps = make_np_array(file_name)
plot(bigsteps)
#os.remove(filename)