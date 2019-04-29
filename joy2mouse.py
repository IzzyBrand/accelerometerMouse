import time
import uinput
import numpy as np
import Adafruit_ADS1x15
import RPi.GPIO as GPIO

LEFT_BTN_PIN = 23
RIGHT_BTN_PIN = 24
STOP_BTN_PIN = 25

mins = np.array([0,0])
mids = np.array([1200, 1188])
maxs = np.array([2047, 2047])

deadzone = 10
deadzones_upper = mids + deadzone
deadzones_lower = mids - deadzone

max_command = 15

directions = np.array([1, -1])

mouse_active = False

if __name__ == '__main__':
    # setup the mouse control
    device = uinput.Device([
            uinput.BTN_LEFT,
            uinput.BTN_RIGHT,
            uinput.REL_X,
            uinput.REL_Y,
            ])

    # setup the ADC
    adc = Adafruit_ADS1x15.ADS1015()
    GAIN = 1

    # setup the GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LEFT_BTN_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(RIGHT_BTN_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(STOP_BTN_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    prev_buttons = np.array([1, 1, 1])

    old_t = time.time()
    while True:
        # calculate the elapsed time
        new_t = time.time()
        dt = new_t - old_t
        old_t = new_t

        # read the ADC and calculate mouse momvement commands
        vals = np.array([adc.read_adc(1, GAIN),adc.read_adc(0, GAIN)])
        above_deadzone = vals > deadzones_upper
        below_deadzone = vals < deadzones_lower
        above_command = np.floor(max_command * (vals - deadzones_upper) / (maxs - deadzones_upper))
        below_command = np.ceil(max_command * (vals - deadzones_lower) / (deadzones_lower - mins))
        x_command, y_command = directions * (above_deadzone * above_command + below_deadzone * below_command)


        buttons = np.array([GPIO.input(LEFT_BTN_PIN), GPIO.input(RIGHT_BTN_PIN), GPIO.input(STOP_BTN_PIN)], dtype=int)
        left_click, right_click, stop_click = buttons > prev_buttons # detect button release
        prev_buttons = buttons

        if stop_click: mouse_active = not mouse_active

        # print("{}\t{}\t{}".format(left_click, right_click, stop_click))

        if mouse_active:
            device.emit(uinput.REL_X, int(x_command))
            device.emit(uinput.REL_Y, int(y_command))

        print int(x_command), int(y_command)

        if left_click: device.emit_click(uinput.BTN_LEFT)
        if right_click: device.emit_click(uinput.BTN_RIGHT)

        time.sleep(0.02)
