###############################################################################
## File: main.py
## Desc: Main program
## Project: WaterDispenser for Element14 Presents
## License: 
##
## By: Kaleb Clark (KalebTheMaker)
###############################################################################
from pitft_touchscreen import pitft_touchscreen
from Valve import Valve
from Button import Button
import pygame
from pygame.locals import *
from time import sleep
import os

# Colors
WHITE   = (255,255,255)
BLACK   = (0, 0, 0)
RED     = (255, 0, 0)
GREEN   = (0, 255, 0)
BLUE    = (0, 0, 255)
AMBER   = (255, 176, 0)
LTAMBER = (255, 204, 0)

# Global Vars
is_running = True
tft = None
lcd = None
btns = []
fonts = {}
btn_id = None

# Env Vars
os.putenv('SDL_FBDEV', '/dev/fb1')

def setup():
    global tft, lcd
    # Instantiate TFT 
    tft = pitft_touchscreen()
    tft.start()

    # Pygame
    pygame.init()
    pygame.mouse.set_visible(False)



    # Fonts
    fonts['16'] = pygame.font.Font(None, 16)
    lcd = pygame.display.set_mode((320, 240))

    # Setup Screen
    lcd.fill(BLACK)
    pygame.display.update()

def drawGeometry():
    pygame.draw.line(lcd, GREEN, (0, 179), (340, 179))
    pygame.draw.line(lcd, GREEN, (212, 179), (212, 0))
    pygame.display.update()

def main():
    #print(tft)
    pass

def detectButtonPush():
    global tft, btns, btn_id
    #bid = None
    while not tft.queue_empty():
        for e in tft.get_event():
            #print(e)
            if e['x'] is not None and e['y'] is not None and e['touch'] == 1:
                #print("Down")
                for b in btns:
                    x, y = e['x'], e['y']
                    if x >= b.left and x <= (b.left + b.width):
                        if y >= b.top and y <= (b.top + b.height):
                            btn_id = b.id
                            return b.id
            # elif e['touch'] == 0:
            #     #print("UP")
            #     return btn_id

# Main Execution ==============================================================
if __name__ == '__main__':
    setup()
    drawGeometry()
    btns.append(Button(0, lcd, AMBER, LTAMBER, fonts['16'], "GO", 5, 100, 200, 70))
    btns.append(Button(1, lcd, AMBER, LTAMBER, fonts['16'], "Cold Valve", 220, 125, 100, 45))
    btns.append(Button(2, lcd, AMBER, LTAMBER, fonts['16'], "Hot Valve", 220, 75, 100, 45))
    btns.append(Button(3, lcd, AMBER, LTAMBER, fonts['16'], "Hot Status", 220, 5, 100, 65))

    # Valves
    vhot = Valve(5)
    vcold = Valve(6)

    try:
        while is_running:
            main()

            # TFT Buttons
            btn_id = detectButtonPush()     # Maybe disable when waiting for btn to complete.
            if btn_id is not None:
                print(btn_id)
                if btn_id == 0:     # GO BUTTON PUSHED
                    sleep(2)
                    btn_id = None
                elif btn_id == 1:   # COLD VALVE BUTTON PUSHED
                    vcold.toggle()
                    btns[btn_id].state = vcold.state
                    btns[btn_id].draw()
                    btn_id = None
                elif btn_id == 2:   # HOT VAVLE BUTTON PUSHED
                    vhot.toggle()
                    btns[btn_id].state = vhot.state
                    btns[btn_id].draw()
                    btn_id = None
                elif btn_id == 3:   # HOT STATUS BUTTON PUSHED
                    sleep(2)
                    btn_id = None
                
                btn_id = None

    except KeyboardInterrupt:
        print("CTRL-C Initiated. Deconstructing Universe")
        tft.stop()
        quit()