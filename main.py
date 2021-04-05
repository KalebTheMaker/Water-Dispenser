###############################################################################
## File: main.py
## Desc: Main program
## Project: WaterDispenser for Element14 Presents
## License: 
##
## By: Kaleb Clark (KalebTheMaker)
###############################################################################
from WDDisplay import WDDisplay
from Valve import Valve
from pitft_touchscreen import pitft_touchscreen

# Global vars
handling_button = False
active_button = None

## Main Program
if __name__ == '__main__':
    t = pitft_touchscreen()
    t.start()

    vhot    = Valve(5)
    vcold   = Valve(6)
    
    lcd = WDDisplay()
    lcd.drawFavButtons()
    lcd.drawStaticButtons()
    print(lcd.btns)
    lcd.update()

    try: 
        while True:
            # Handle touchscreen inputs
            if not handling_button:
                while not t.queue_empty():
                    for e in t.get_event():
                        if e['x'] is not None and e['y'] is not None:
                            handling_button = True
                            active_button = lcd.buttonClick(e)
                            # print(getButton(e, 0, 200, 75, 40))
                            #print(lcd.buttonClick(e))

            # Handle button events
            if active_button is not None:
                print(active_button)
                active_button = None
            
            handling_button = False

    except KeyboardInterrupt:
        print("CTRL-C initiated. Deconstructing the universe")
        t.stop()
        quit()


