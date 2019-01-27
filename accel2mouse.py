import time
import uinput
from mpu6050 import mpu6050
import numpy as np

NUM_CALIBRATION_SAMPLES = 200

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
    offset_alpha = 0.01

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
        accel = np.array([raw['x'], raw['y']])
        offset = offset_alpha * accel + (1 - offset_alpha) * offset
        accel -= offset

        # update the mouse velocity estimate
        vel += accel * dt
        vel *= 0.999 

        # get a command from the velocity
        x_command = int(vel[1] * 50)
        y_command =  int(vel[0] * 50)
        print x_command, y_command

        device.emit(uinput.REL_X, x_command)
        device.emit(uinput.REL_Y, y_command)