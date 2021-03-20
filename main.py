###############################################################################
## File: main.py
## Desc: Main program
## Project: WaterDispenser for Element14 Presents
## License: 
##
## By: Kaleb Clark (KalebTheMaker)
###############################################################################
from WDDisplay import WDDisplay

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


