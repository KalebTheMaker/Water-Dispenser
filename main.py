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
from Relay import Relay
from KTMTimer import KTMTimer
import pygame
from pygame.locals import *
import time
import os
import redis



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
r = None
btns = []
fonts = {}
btn_id = None
heater_elapsed = 0
heat_timer_secs = 300      # Number of seconds to preheat water
fav0_timer_secs = 25
fav1_timer_secs = 34
fav2_timer_secs = 15
fav3_timer_secs = 16

# Valve
vhot = Valve(5, 1080, 1500)
vhot.close()
vcold = Valve(6, 1080, 1500)
vcold.close()
relay = Relay(21)
relay.off()

# Env Vars
os.putenv('SDL_FBDEV', '/dev/fb1')


def setup():
    global tft, lcd, r
    # Instantiate TFT 
    tft = pitft_touchscreen()
    tft.start()

    # Pygame
    pygame.init()
    pygame.mouse.set_visible(False)

    # Redis
    r = redis.Redis(host="localhost", decode_responses=True)
    r.set('heatState', 'False')

    # Fonts
    fonts['16'] = pygame.font.Font(None, 16)
    fonts['24'] = pygame.font.Font(None, 24)
    lcd = pygame.display.set_mode((320, 240))

    # Setup Screen
    lcd.fill(BLACK)
    pygame.display.update()

def drawGeometry():
    pygame.draw.line(lcd, GREEN, (0, 179), (340, 179))
    pygame.draw.line(lcd, GREEN, (212, 179), (212, 0))
    pygame.display.update()

def main():
    pass

def eStop():
    vhot.close()
    vcold.close()
    relay.off()
    r.set('heatState', 'False')
    for b in btns:
        b.state = False
        b.draw()


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


def endtimer():
    global relay
    print("TimerStop")
    relay.off()
    btns[3].state = relay.state
    r.set('heatState', str(relay.state))
    btns[3].draw()

def fav0End():
    print("Fav0 End")
    vhot.close()
    btns[4].state = vhot.state
    btns[4].draw()

def fav1End():
    print("Fav1 End")
    vcold.close()
    btns[5].state = vcold.state
    btns[5].draw()

def fav2End():
    print("Fav2 End")
    vhot.close()
    btns[6].state = vhot.state
    btns[6].draw()

def fav3End():
    print("Fav3 End")
    vcold.close()
    btns[7].state = vcold.state
    btns[7].draw()

# Timers
heat_timer = KTMTimer(heat_timer_secs, endtimer)
fav0_timer = KTMTimer(fav0_timer_secs, fav0End)
fav1_timer = KTMTimer(fav1_timer_secs, fav1End)
fav2_timer = KTMTimer(fav2_timer_secs, fav2End)
fav3_timer = KTMTimer(fav3_timer_secs, fav3End)


# Main Execution ==============================================================
if __name__ == '__main__':
    setup()
    drawGeometry()

    # Draw Control Buttons
    btns.append(Button(0, lcd, AMBER, RED, fonts['24'], "E STOP", 5, 100, 200, 70))
    btns.append(Button(1, lcd, AMBER, LTAMBER, fonts['16'], "Cold Water", 220, 125, 100, 45))
    btns.append(Button(2, lcd, AMBER, LTAMBER, fonts['16'], "Hot Water", 220, 75, 100, 45))
    btns.append(Button(3, lcd, AMBER, LTAMBER, fonts['16'], "Heating", 220, 5, 100, 65))

    # Favorite Buttons
    btns.append(Button(4, lcd, AMBER, LTAMBER, fonts['16'], "F. Press", 5, 190, 75, 40))
    btns.append(Button(5, lcd, AMBER, LTAMBER, fonts['16'], "Water Bottle", 83, 190, 75, 40))
    btns.append(Button(6, lcd, AMBER, LTAMBER, fonts['16'], "Coffee Cup", 161, 190, 75, 40))
    btns.append(Button(7, lcd, AMBER, LTAMBER, fonts['16'], "Pint Glass", 239, 190, 75, 40))


    try:
        while is_running:
            main()

            # TFT Buttons
            btn_id = detectButtonPush()     # Maybe disable when waiting for btn to complete.

            if btn_id is not None:
                # print(btn_id)
                if btn_id == 0:     # GO BUTTON PUSHED
                    eStop()
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
                    relay.toggle()
                    btns[btn_id].state = relay.state
                    r.set('heatState', str(relay.state))
                    if relay.state == True:
                        print("Creating timer")
                        heat_timer.start()

                    btns[btn_id].draw()
                    btn_id = None
                elif btn_id == 4:    # Fav0 button
                    print("Fav0 Pushed")
                    vhot.open()
                    btns[btn_id].state = vhot.state
                    btns[btn_id].draw()
                    fav0_timer.start()
                elif btn_id == 5:   # Fav1 button
                    print("Fav1 pushed")
                    vcold.open()
                    btns[btn_id].state = vcold.state
                    btns[btn_id].draw()
                    fav1_timer.start()
                elif btn_id == 6:   # Fav2 Button
                    print("Fav2 pushed")
                    vhot.open()
                    btns[btn_id].state = vhot.state
                    btns[btn_id].draw()
                    fav2_timer.start()
                elif btn_id == 7:   # Fav3 Button
                    print("Fav3 pushed")
                    vcold.open()
                    btns[btn_id].state = vcold.state
                    btns[btn_id].draw()
                    fav3_timer.start()
                
                btn_id = None

            # Control Heating element from redis & cron job
            # Heat button/status is button id 3
            hs = r.get('heatState')
            if hs == "True" and btns[3].state == False:
                relay.on()
                btns[3].state = relay.state
                btns[3].draw()
            elif hs == "False" and btns[3].state == True:
                relay.off()
                btns[3].state = relay.state
                btns[3].draw()

            if hs == "True":
                heater_elapsed = heat_timer.remaining()
                print(heater_elapsed)

    except KeyboardInterrupt:
        print("CTRL-C Initiated. Deconstructing Universe")
        tft.stop()
        relay.cleanup()
        quit()