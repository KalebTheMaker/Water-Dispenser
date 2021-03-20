## Valve.py
## Class for controlling valves in the Water Dispenser project for Element15
## 
## By: Kaleb Clark (KalebTheMaker)
import pigpio
import time

class Valve(object):
    def __init__(self, iopin):
        self.pio = pigpio.pi()
        self.iopin = iopin
        self.open_val = 500
        self.close_val = 1500

    def open(self):
        self.pio.set_servo_pulsewidth(self.iopin, 500)

    def close(self):
        self.pio.set_servo_pulsewidth(self.iopin, 1500)
