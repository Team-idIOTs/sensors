import matplotlib.pyplot as plt
import numpy as np
# Read your data

def make_np_array(filename):
    with open(filename) as f:
        data = f.readlines()
        data = np.asarray([x[:-1].split(",") for x in data])
        return data

def plot(data):
    accelx = data[:,0].astype(float)
    accely = data[:,1].astype(float)
    accelz = data[:,2].astype(float)

    gyrox = data[:,3].astype(float)
    gyroy = data[:,4].astype(float)
    gyroz = data[:,5].astype(float)

    t = accelx.shape[0]
    t = np.arange(0., t)

    plt.figure(0)

    accelxline, =  plt.plot(t, accelx, label="Accel X")
    accelyline, =  plt.plot(t, accely, label="Accel Y")
    accelzline, =  plt.plot(t, accelz, label="Accel Z")

    plt.legend(handles=[accelxline, accelyline, accelzline], loc='lower right')

    plt.figure(1)

    gyroxline, =  plt.plot(t, gyrox, label="Gyro X")
    gyroyline, =  plt.plot(t, gyroy, label="Gyro Y")
    gyrozline, =  plt.plot(t, gyroz, label="Gyro Z")

    plt.legend(handles=[gyroxline, gyroyline, gyrozline], loc='lower right')
    plt.show()



bigsteps = make_np_array('data/data4_22_1_bigsteps')
smallsteps = make_np_array('data/data4_22_1_smallsteps')

plot(bigsteps)
