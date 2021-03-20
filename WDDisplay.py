import pygame
from pygame.locals import *
import os
from time import sleep
from pitft_touchscreen import pitft_touchscreen

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

class WDDisplay(object):
    """ Class for rendering viewable elements and handling button clicks"""
    def __init__(self):
        self.buttons = []
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
        pygame.display.update()

    # -------------------------------------------------------------------------
    def favButtons(self):
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
    def click(self, t):
        """Experimental event handler
        Parameters: 
            t (obj): tft object
        """
        while not t.queue_empty():
            for e in t.get_event():
                if e['x'] is not None and e['y'] is not None:
                    return e