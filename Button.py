###############################################################################
## File: Button.py
## Desc: Class for handling Buttons.
## Project: WaterDispenser for Element14 Presents
## License: 
##
## By: Kaleb Clark (KalebTheMaker)
###############################################################################
import pygame

class Button(object):
    """Class for handling button pushes on LCD"""
    def __init__(self, id, lcd, box_color, text_color, font, caption, left, top, width, height):
        """Init Button class
        Parameters: None
        """
        self.id = id
        self.lcd = lcd
        self.box_color = box_color
        self.text_color = text_color
        self.font = font
        self.caption = caption
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.state = False
        self.draw()

    def draw(self):
        self.destroy()
        fill = 1
        txt_color = self.text_color

        if self.state:
            fill = 0
            txt_color = (0, 0, 0)

        btn_rect = pygame.draw.rect(
            self.lcd, (self.box_color),
            (self.left, self.top, self.width, self.height),
            fill
        )
        t_w, t_h = self.font.size(self.caption)
        top = self.top + (self.height/2)-(t_h/2)
        left = self.left + (self.width/2)-(t_w/2)
        self.lcd.blit(self.font.render(self.caption, True, (txt_color)), (left, top))
        pygame.display.update()

    def destroy(self):
        btn_rect = pygame.draw.rect(
            self.lcd, (0,0,0), 
            (self.left, self.top, self.width, self.height),
            0
        )


        