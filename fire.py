

import time
import random
from cosmic import CosmicUnicorn


class Fire:
    def __init__(self, context):
        self.context = context
        self.width = CosmicUnicorn.WIDTH + 2
        self.height = CosmicUnicorn.HEIGHT + 4
        self.heat = [[0.0 for y in range(self.height)] for x in range(self.width)]
        self.fire_spawns = 5
        self.damping_factor = 0.97

        self.fire_colours = [
            context.graphics.create_pen(0, 0, 0),
            context.graphics.create_pen(20, 20, 20),
            context.graphics.create_pen(180, 30, 0),
            context.graphics.create_pen(220, 160, 0),
            context.graphics.create_pen(255, 255, 180)]
        
    def enter(self):
        print(f'Fire Entry')
        self.context.set_brightness(0.5)

    def refresh_display(self):
        self._update()
        self._draw()
        
    def button_pressed(self):
        pass

    @micropython.native  # noqa: F821
    def _update(self):
        _heat = self.heat

        # clear the bottom row and then add a new fire seed to it
        for x in range(self.width):
            _heat[x][self.height - 1] = 0.0
            _heat[x][self.height - 2] = 0.0

        for c in range(self.fire_spawns):
            x = random.randint(0, self.width - 4) + 2
            _heat[x + 0][self.height - 1] = 1.0
            _heat[x + 1][self.height - 1] = 1.0
            _heat[x - 1][self.height - 1] = 1.0
            _heat[x + 0][self.height - 2] = 1.0
            _heat[x + 1][self.height - 2] = 1.0
            _heat[x - 1][self.height - 2] = 1.0

        factor = self.damping_factor / 5.0
        for y in range(0, self.height - 2):
            for x in range(1, self.width - 1):
                _heat[x][y] += _heat[x][y + 1] + _heat[x][y + 2] + _heat[x - 1][y + 1] + _heat[x + 1][y + 1]
                _heat[x][y] *= factor

    @micropython.native  # noqa: F821
    def _draw(self):
        _graphics = self.context.graphics
        _heat = self.heat
        _set_pen = _graphics.set_pen
        _pixel = _graphics.pixel
        _fire_colours = self.fire_colours

        for y in range(CosmicUnicorn.HEIGHT):
            for x in range(CosmicUnicorn.WIDTH):
                value = _heat[x + 1][y]
                if value < 0.15:
                    _set_pen(_fire_colours[0])
                elif value < 0.25:
                    _set_pen(_fire_colours[1])
                elif value < 0.35:
                    _set_pen(_fire_colours[2])
                elif value < 0.45:
                    _set_pen(_fire_colours[3])
                else:
                    _set_pen(_fire_colours[4])
                _pixel(x, y)

        self.context.update_display()
