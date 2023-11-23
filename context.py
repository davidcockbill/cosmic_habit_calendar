#!/usr/bin/env python3

import machine
from cosmic import CosmicUnicorn
from picographics import PicoGraphics, DISPLAY_COSMIC_UNICORN as DISPLAY

class Context:
    def __init__(self):
        self.cu = CosmicUnicorn()
        self.graphics = PicoGraphics(DISPLAY)
        self.rtc = machine.RTC()

        self.pens = {
            'white': self.graphics.create_pen(255, 255, 255),
            'black': self.graphics.create_pen(0, 0, 0),
            'blue': self.graphics.create_pen(0, 0, 255),
            'dark_blue': self.graphics.create_pen(0, 0, 20),
            'dark_background_blue': self.graphics.create_pen(0, 0, 10),
            'green': self.graphics.create_pen(0, 255, 0),
            'dark_green': self.graphics.create_pen(0, 80, 0),
            'pink': self.graphics.create_pen(255, 20, 147),
            'orange': self.graphics.create_pen(255, 102, 0),
            'light_grey': self.graphics.create_pen(20, 20, 20),
        }

        self.set_brightness(0.8)
        self.graphics.set_font('bitmap8')

    def datetime(self):
        return self.rtc.datetime()

    def update_display(self):
        self.cu.update(self.graphics)

    def set_brightness(self, brightness):
        self.cu.set_brightness(brightness)

    def clear_display(self, background):
        self.set_pen(background)
        self.graphics.clear()

    def set_pen(self, pen):
        self.graphics.set_pen(pen)

    def white(self):
        return self.pens.get('white')
    
    def black(self):
        return self.pens.get('black')

    def blue(self):
        return self.pens.get('blue')
    
    def dark_blue(self):
        return self.pens.get('dark_blue')
    
    def dark_background_blue(self):
        return self.pens.get('dark_background_blue')

    def green(self):
        return self.pens.get('green')
    
    def dark_green(self):
        return self.pens.get('dark_green')
    
    def pink(self):
        return self.pens.get('pink')
        
    def orange(self):
        return self.pens.get('orange')
    
    def light_grey(self):
        return self.pens.get('light_grey')
