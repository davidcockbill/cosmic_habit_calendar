#!/usr/bin/env python3

import time
import network
import ntptime

from cosmic import CosmicUnicorn

from context import Context
from habit_calendar import HabitCalendar
from wifi import WIFI_SSID, WIFI_PASSWORD

context = Context()
habit_calendar = HabitCalendar(context)


def sync_time():
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
        display_wifi(brightness=brightness)
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


def display_wifi(brightness=0.5):
    foreground=context.blue()
    background=context.black()
    context.set_brightness(brightness)
    context.clear_display(background)

    centre_x = 16
    centre_y = 22
    radius = 18

    # Concentric rings
    context.graphics.set_pen(foreground)
    context.graphics.circle(centre_x, centre_y, 17)
    context.set_pen(background)
    context.graphics.circle(centre_x, centre_y, 15)
    context.set_pen(foreground)
    context.graphics.circle(centre_x, centre_y, 12)
    context.set_pen(background)
    context.graphics.circle(centre_x, centre_y, 10)
    context.set_pen(foreground)
    context.graphics.circle(centre_x, centre_y, 7)
    context.set_pen(background)
    context.graphics.circle(centre_x, centre_y, 5)

    # Cut off bottom of rings
    context.graphics.rectangle(0, centre_y+1, 32, 32)

    #  Clear to 45 degrees
    context.set_pen(background)
    context.graphics.triangle(centre_x, centre_y+1, centre_x-radius, centre_y+1, centre_x-radius, centre_y-radius)
    context.graphics.triangle(centre_x, centre_y+1, centre_x+radius, centre_y+1, centre_x+radius, centre_y-radius)

    # Centre circle
    context.graphics.set_pen(foreground)
    context.graphics.circle(centre_x, centre_y, 2)

    context.update_display()


def process_button(button):
    initial_timestamp = time.ticks_ms()
    if context.cu.is_pressed(button):
        while context.cu.is_pressed(button):
            time.sleep(0.01)
    duration = time.ticks_ms() - initial_timestamp
    return duration


def loop():
    duration = process_button(CosmicUnicorn.SWITCH_A)
    if duration > 100:
        if duration < 1000:
            habit_calendar.button_pressed()
        else:
            print(f'Long push {duration}')

    habit_calendar.refresh_display()


if __name__ == "__main__":
    sync_time()
    while True:
        loop()
        time.sleep(0.01)
