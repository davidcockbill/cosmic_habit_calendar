#!/usr/bin/env python3


class Color:
    def __init__(self, graphics):
        self.graphics = graphics

    def white(self):
        return self.graphics.create_pen(255, 255, 255)
    
    def black(self):
        return self.graphics.create_pen(0, 0, 0)

    def blue(self):
        return self.graphics.create_pen(0, 0, 255)

    def dark_blue(self):
        return self.graphics.create_pen(0, 0, 20)
    
    def dark_background_blue(self):
        return self.graphics.create_pen(0, 0, 10)

    def green(self):
        return self.graphics.create_pen(0, 255, 0)
    
    def dark_green(self):
        return self.graphics.create_pen(0, 80, 0)
    
    def pink(self):
        return self.graphics.create_pen(255, 20, 147)
        
    def orange(self):
        return self.graphics.create_pen(255, 102, 0)
    
    def light_grey(self):
        return self.graphics.create_pen(20, 20, 20)
    
