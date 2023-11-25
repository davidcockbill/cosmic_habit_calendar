#!/usr/bin/env python3


class Brightness:
    def __init__(self, context):
        self.context = context

    def enter(self):
        print(f'Brightness Entry')
        self.context.clear_display()
        self.context.update_display()

    def refresh_display(self):
        self.context.set_pen(self.context.orange())
        self.context.graphics.text('Lux', 3, 2, scale=1, spacing=1)
        self.context.update_display()

    def button_pressed(self):
        print(f'Increment brightness')
        self.context.increment_brightness()
