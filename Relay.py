###############################################################################
## File: Relay.py
## Desc: Class for controlling Relays
## Project: WaterDispenser for Element14 Presents
## License: 
##
## By: Kaleb Clark (KalebTheMaker)
###############################################################################
import RPi.GPIO as GPIO
import time

class Relay(object):
    def __init__(self, iopin):
        self.iopin = iopin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.iopin, GPIO.OUT)
        self.state = False

    def on(self):
        GPIO.output(self.iopin, GPIO.HIGH)
        self.state = True


    def off(self):
        GPIO.output(self.iopin, GPIO.LOW)
        self.state = False

    def toggle(self):
        if self.state == True:
            self.off()
        elif self.state == False:
            self.on()


# relay = Relay(21)
# relay.on()
# time.sleep(1)
# relay.off()