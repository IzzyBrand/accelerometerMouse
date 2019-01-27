import time
import uinput
from config import *
from mpu6050 import mpu6050
import numpy as np


if __name__ == '__main__':
    mpu = mpu6050(0x68)
    device = uinput.Device([
            uinput.BTN_LEFT,
            uinput.BTN_RIGHT,
            uinput.REL_X,
            uinput.REL_Y,
            ])

    total = np.zeros(2)
    for i in range(NUM_CALIBRATION_SAMPLES):
        raw = mpu.get_accel_data()
        total += np.array([raw['x'], raw['y']])

    offset = total/NUM_CALIBRATION_SAMPLES

    print '[Calibrated] X: {}\tY: {}'.format(offset[0], offset[1])

    vel = np.zeros(2)

    old_t = time.time()
    while True:
        # calculate the elapsed time
        new_t = time.time()
        dt = new_t - old_t
        old_t = new_t

        # read the accelerometer
        raw = mpu.get_accel_data()
        accel = np.array([raw['x'], raw['y']]) - offset

        # update the mouse velocity estimate
        vel += accel * dt * MOUSE_SCALAR
        vel *= 0.95 
        print vel

        device.emit(uinput.REL_X, int(vel[1]))
        device.emit(uinput.REL_Y, -int(vel[0]))