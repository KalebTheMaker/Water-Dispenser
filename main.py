## main.py
## Main python program for the Water dispenser project for Element14 Presents
##
## By: Kaleb Clark (KalebTheMaker)
import pygame
from pygame.locals import *
import os
from time import sleep
from pitft_touchscreen import pitft_touchscreen
from WDDisplay import WDDisplay

# Colors
WHITE   = (255,255,255)
BLACK   = (0, 0, 0)
RED     = (255, 0, 0)
GREEN   = (0, 255, 0)
BLUE    = (0, 0, 255)
AMBER   = (255, 176, 0)
LTAMBER = (255, 204, 0)

os.putenv('SDL_FBDEV', '/dev/fb1')
# os.putenv('SDL_MOUSEDRV', 'TSLIB')
# os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen')

fav_buttons = ['F. Press', 'Bottle', 'Pint', 'Coffee Cup']




## Test BS
def getButton(e, left, top, width, height):
    x, y = e['x'], e['y']
    #print("X: %d, Y: %d" % (x, y))
    if x >= left and x <= (left+width):
        if y >= top and y <= (top+height):
            return True
    
    return False

## Main Program
if __name__ == '__main__':
    t = pitft_touchscreen()
    t.start()
    lcd = WDDisplay()
    lcd.favButtons()

    print(lcd.buttons)

    try: 
        while True:
            lcd.click(t)
            # while not t.queue_empty():
            #     for e in t.get_event():
            #         if e['x'] is not None and e['y'] is not None:
            #             print(getButton(e, 0, 200, 75, 40))

    except KeyboardInterrupt:
        print("CTRL-C initiated. Deconstructing the universe")
        t.stop()
        quit()


