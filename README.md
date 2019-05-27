# accelerometerMouse
A proof of concept project for a novel computer UI

```
pip install python-uinput mpu6050-raspberrypi
```

`mouseController` contains an Arduino sketch to read from the joystick and buttons and control the mouse. The arduino emulates a mouse when plugged into a computer via usb. Therefore you have to press the reset button to take the arduino out of "usb emulator mode" and allow sketches to be uploaded to it. With the sketch uplodated, on boot the arduino is emulating a mouse by default.

`joy2mouse.py` is a python script to be run on raspberry pi. This controls the mouse position on the raspberry py. Ths script can be run from the commandline with `sudo python joy2mouse.py`.