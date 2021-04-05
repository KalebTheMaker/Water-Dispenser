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
        self.state = False
        self.close()

    def open(self):
        self.pio.set_servo_pulsewidth(self.iopin, 500)
        self.state = True

    def close(self):
        self.pio.set_servo_pulsewidth(self.iopin, 1500)
        self.state = False

    def toggle(self):
        if self.state == True:
            self.close()
        elif self.state == False:
            self.open()