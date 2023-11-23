#!/usr/bin/env python3

import time
import network
import ntptime
from wifi_config import WIFI_SSID, WIFI_PASSWORD


class Wifi:
    def __init__(self, context):
        self.context = context

    def sync_time(self):
        last_timestamp = time.ticks_ms()
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)

        connection_check_duration = 500
        retry = 0
        while True:
            timestamp = time.ticks_ms()
            if timestamp - last_timestamp > connection_check_duration:
                last_timestamp = timestamp
                if wlan.status() < 0 or wlan.status() >= 3:
                    break
                print(f'[{retry}] Waiting for wifi connection...')

            brightness = [0.5, 0.4, 0.3, 0.2, 0.1, 0.2, 0.3, 0.4][retry%8]
            self._display_wifi(brightness=brightness)
            time.sleep(0.1)
            retry += 1
        print('Connected')

        while True:
            print(f'Setting time...')
            try:
                ntptime.settime()
                print(f'Time set')
                break
            except OSError:
                pass
            time.sleep(0.05)

        wlan.disconnect()
        wlan.active(False)


    def _display_wifi(self, brightness=0.5):
        foreground=self.context.blue()
        background=self.context.black()
        self.context.set_brightness(brightness)
        self.context.clear_display(background)

        centre_x = 16
        centre_y = 22
        radius = 18

        # Concentric rings
        self.context.graphics.set_pen(foreground)
        self.context.graphics.circle(centre_x, centre_y, 17)
        self.context.set_pen(background)
        self.context.graphics.circle(centre_x, centre_y, 15)
        self.context.set_pen(foreground)
        self.context.graphics.circle(centre_x, centre_y, 12)
        self.context.set_pen(background)
        self.context.graphics.circle(centre_x, centre_y, 10)
        self.context.set_pen(foreground)
        self.context.graphics.circle(centre_x, centre_y, 7)
        self.context.set_pen(background)
        self.context.graphics.circle(centre_x, centre_y, 5)

        # Cut off bottom of rings
        self.context.graphics.rectangle(0, centre_y+1, 32, 32)

        #  Clear to 45 degrees
        self.context.set_pen(background)
        self.context.graphics.triangle(centre_x, centre_y+1, centre_x-radius, centre_y+1, centre_x-radius, centre_y-radius)
        self.context.graphics.triangle(centre_x, centre_y+1, centre_x+radius, centre_y+1, centre_x+radius, centre_y-radius)

        # Centre circle
        self.context.graphics.set_pen(foreground)
        self.context.graphics.circle(centre_x, centre_y, 2)

        self.context.update_display()