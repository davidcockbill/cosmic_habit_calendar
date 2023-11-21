#!/usr/bin/env python3

import time
import machine
import network
import ntptime
from cosmic import CosmicUnicorn
from picographics import PicoGraphics, DISPLAY_COSMIC_UNICORN as DISPLAY
from habit_calendar import HabitCalendar
from color import Color
from wifi import WIFI_SSID, WIFI_PASSWORD

rtc = machine.RTC()
cu = CosmicUnicorn()
graphics = PicoGraphics(DISPLAY)
color = Color(graphics)
habit_calendar = HabitCalendar(graphics, cu, rtc)


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
        display_wifi(brightness=brightness, foreground=color.blue())
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


def clear_display(background):
    graphics.set_pen(background)
    graphics.clear()


def display_wifi(brightness=0.5, foreground=color.white(), background=color.black()):
    cu.set_brightness(brightness)
    clear_display(background)

    centre_x = 16
    centre_y = 22
    radius = 18

    # Concentric rings
    graphics.set_pen(foreground)
    graphics.circle(centre_x, centre_y, 17)
    graphics.set_pen(background)
    graphics.circle(centre_x, centre_y, 15)
    graphics.set_pen(foreground)
    graphics.circle(centre_x, centre_y, 12)
    graphics.set_pen(background)
    graphics.circle(centre_x, centre_y, 10)
    graphics.set_pen(foreground)
    graphics.circle(centre_x, centre_y, 7)
    graphics.set_pen(background)
    graphics.circle(centre_x, centre_y, 5)

    # Cut off bottom of rings
    graphics.rectangle(0, centre_y+1, 32, 32)

    #  Clear to 45 degrees
    graphics.set_pen(background)
    graphics.triangle(centre_x, centre_y+1, centre_x-radius, centre_y+1, centre_x-radius, centre_y-radius)
    graphics.triangle(centre_x, centre_y+1, centre_x+radius, centre_y+1, centre_x+radius, centre_y-radius)

    # Centre circle
    graphics.set_pen(foreground)
    graphics.circle(centre_x, centre_y, 2)

    cu.update(graphics)


def process_button(button):
    initial_timestamp = time.ticks_ms()
    if cu.is_pressed(button):
        while cu.is_pressed(button):
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
    
    if cu.is_pressed(CosmicUnicorn.SWITCH_BRIGHTNESS_UP):
        cu.adjust_brightness(+0.1)
        habit_calendar.update_display()

    if cu.is_pressed(CosmicUnicorn.SWITCH_BRIGHTNESS_DOWN):
        cu.adjust_brightness(-0.1)
        habit_calendar.update_display()

    habit_calendar.refresh_display()


def initialise():
    print(f'Initialising...')
    cu.set_brightness(0.8)
    graphics.set_font('bitmap8')
    print(f'Initialised')


if __name__ == "__main__":
    sync_time()
    initialise()
    while True:
        loop()
        time.sleep(0.01)
