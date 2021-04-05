###############################################################################
## File: WDDisplay.py
## Desc: Class for handling display and button pushes.
## Project: WaterDispenser for Element14 Presents
## License: 
##
## By: Kaleb Clark (KalebTheMaker)
###############################################################################
import pygame
from pygame.locals import *
import os
from time import sleep


# Colors
WHITE   = (255,255,255)
BLACK   = (0, 0, 0)
RED     = (255, 0, 0)
GREEN   = (0, 255, 0)
BLUE    = (0, 0, 255)
AMBER   = (255, 176, 0)
LTAMBER = (255, 204, 0)

os.putenv('SDL_FBDEV', '/dev/fb1')

fav_buttons = [
    'F. Press',     # 0 
    'Bottle',       # 1
    'Pint',         # 2
    'Coffee Cup'    # 3
]

class Button(object):
    """Class for buttons"""
    def __init__(self, parent, caption, left, top, width, height):
        """ Instantiate new button
        Parameters:
            caption (str): Text in the button
            left (int): Left position of the rectangle
            top (int): Right position of the rectangle
            width (int): Width of the button
            height (int): Height of the button
        """
        self.parent = parent
        self.caption = caption
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.active = False
        self.draw()

    def draw(self):
        """Draw the button"""
        btn_rect = pygame.draw.rect(
            self.parent.screen, (LTAMBER), 
            (self.left, self.top, self.width, self.height), 
            1
        )
        t_w, t_h = self.parent.font.size(self.caption)
        top = self.top + (self.height/2)-(t_h/2)
        left = self.left + (self.width/2)-(t_w/2)
        self.parent.screen.blit(
            self.parent.font.render(self.caption, True, (AMBER)),
            (left, top)
        )

class WDDisplay(object):
    """ Class for rendering viewable elements and handling button clicks"""
    def __init__(self):
        self.buttons = []
        self.btns = []
        self.fav_geom = [5, 190, 75, 40, 4] # left, top, width, height, space
        pygame.init()
        pygame.mouse.set_visible(False)
        self.font = pygame.font.Font(None, 16)
        self.screen = pygame.display.set_mode((320, 240))
        self.screen.fill(BLACK)
        pygame.display.update()

    # -------------------------------------------------------------------------
    def addButton(self, caption, l, t, w, h):
        """Draws button on screen
        Parameters:
           caption (str): The caption in the button
           l (int): Left position
           t (int): Top Position
           w (int): Width of rectangle
           h (int): Height of rectangle
        """
        rect = pygame.draw.rect(self.screen, (LTAMBER), (l, t, w, h), 1)
        t_w, t_h = self.font.size(caption)
        top = t + (h/2)-(t_h/2)
        left = l + (w/2)-(t_w/2)
        self.screen.blit(self.font.render(caption, True, (AMBER)), (left, top))
        self.buttons.append({
            'left': l, 'top': t,
            'width': w, 'height': h
        })
        self.drawGeometry()
        pygame.display.update()

    def drawGeometry(self):
        pygame.draw.line(self.screen, GREEN, (0, 179), (340, 179))
        pygame.draw.line(self.screen, GREEN, (212, 179), (212, 0))

    def drawStaticButtons(self):
        # Valve Cold Button
        self.addButton("Cold Valve", 220, 125, 100, 45)
        # Valve Hot Button
        self.addButton("Hot Valve", 220, 75, 100, 45)
        # Hot Water on/off Button
        #self.addButton("Hot Status", 220, 5, 100, 65)
        self.btns.append(Button(self, "Hot Status", 220, 5, 100, 65))
        # Go Button
        #self.addButton("GO", 5, 100, 200, 70)
        self.btns.append(Button(self, "GO", 5, 100, 200, 70))
        
        pygame.display.update()

    def update(self):
        pygame.display.update()
        


    # -------------------------------------------------------------------------
    def drawFavButtons(self):
        """Renders favorite buttons from global list at top of this file.
        Parameters: None
        """
        global fav_buttons
        left, top, width, height, space = self.fav_geom

        for i, cap in enumerate(fav_buttons, start=0):
            l = (left + (i*width))
            if i > 0: l = (l+(i*space))
            # print("I: %d, left: %d" % (i, l))

            self.addButton(cap, l, top, width, height)

    # -------------------------------------------------------------------------
    def buttonClick(self, e):
        for k, v in enumerate(self.buttons):
            x, y = e['x'], e['y']
            if x >= v['left'] and x <= (v['left'] + v['width']):
                if y >= v['top'] and y <= (v['top'] + v['height']):
                    return k
        return False


