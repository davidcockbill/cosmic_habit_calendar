#!/usr/bin/env python3

import time
import machine
import network
import ntptime
from cosmic import CosmicUnicorn
from picographics import PicoGraphics, DISPLAY_COSMIC_UNICORN as DISPLAY
from date_matrix import DateMatrix
from time_display import write_time
from wifi import WIFI_SSID, WIFI_PASSWORD

last_timestamp = time.ticks_ms()
last_refresh_minute = int(0)
rtc = machine.RTC()
cu = CosmicUnicorn()
graphics = PicoGraphics(DISPLAY)
date_matrix = DateMatrix()


MONTHS = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

WHITE = graphics.create_pen(255, 255, 255)
BLACK = graphics.create_pen(0, 0, 0)
BLUE = graphics.create_pen(0, 0, 255)
DARK_BLUE = graphics.create_pen(0, 0, 20)
GREEN = graphics.create_pen(0, 255, 0)
DARK_GREEN = graphics.create_pen(0, 80, 0)
PINK = graphics.create_pen(255, 20, 147)
ORANGE = graphics.create_pen(255, 102, 0)
LIGHT_GREY = graphics.create_pen(20, 20, 20)

ON = BLUE
OFF = LIGHT_GREY
TODAY_ON = GREEN
TODAY_OFF = PINK
MATRIX_BORDER = DARK_BLUE
BACKGROUND = graphics.create_pen(0, 0, 10)


def sync_time():
    global last_timestamp
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(WIFI_SSID, WIFI_PASSWORD)

    connection_check_duration = 100
    retry = 0
    while True:
        timestamp = time.ticks_ms()
        if timestamp - last_timestamp > connection_check_duration:
            last_timestamp = timestamp
            if wlan.status() < 0 or wlan.status() >= 3:
                break
            print(f'[{retry}] Waiting for wifi connection...')

        brightness = [0.5, 0.4, 0.3, 0.2, 0.1, 0.2, 0.3, 0.4][retry%8]
        display_wifi(brightness=brightness, foreground=BLUE)
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


def current_date():
    _, month, day, _, _, _, _, _ = rtc.datetime()
    return month, day


def display_date_matrix():
    current_month, current_day = current_date()
    row = 18

    # Top Border
    graphics.set_pen(MATRIX_BORDER)
    graphics.line(0, row, 32, row)
    row += 1

    # Matrix
    for month in DateMatrix.month_range():
        graphics.set_pen(OFF)
        graphics.line(0, row, 32, row)
        for day in DateMatrix.day_range(month):
            today = day == current_day-1 and month == current_month-1
            column = day
            pen = TODAY_OFF if today else OFF
            if (date_matrix.isSet(month, day)):
                pen = TODAY_ON if today else ON
            graphics.set_pen(pen)
            graphics.pixel(column, row)

        row += 1

    # Bottom Border 
    graphics.set_pen(MATRIX_BORDER)
    graphics.line(0, row, 32, row)

    cu.update(graphics)


def debounce(button, duration=100):
    global last_timestamp
    if cu.is_pressed(button) and time.ticks_ms() - last_timestamp > duration:
        last_timestamp = time.ticks_ms()
        return True
    return False


def display_date():
    month, day = current_date()
    date = f'{MONTHS[month-1]} {day:02}'

    graphics.set_pen(ORANGE)
    graphics.text(date, 3, 2, scale=1, spacing=1)


def display_time():
    global last_refresh_minute
    _, _, _, _, hour, minute, _, _ = rtc.datetime()
    write_time(graphics, DARK_GREEN, BACKGROUND, hour, minute, 7, 11)
    last_refresh_minute = minute


def toogle_day():
    month, day = current_date()
    print(f'Setting month={month}, day={day}')
    date_matrix.toggle(month-1, day-1)
    date_matrix.store()
    display_date_matrix()


def update_display():
    clear_display(BACKGROUND)
    display_date()
    display_time()
    display_date_matrix()
    cu.update(graphics)


def refresh_display():
    global last_refresh_minute
    _, _, _, _, _, current_minute, _, _ = rtc.datetime()
    if current_minute != last_refresh_minute:
        update_display()


def loop():
    if debounce(CosmicUnicorn.SWITCH_A):
        toogle_day()
    
    if cu.is_pressed(CosmicUnicorn.SWITCH_BRIGHTNESS_UP):
        cu.adjust_brightness(+0.1)
        update_display()

    if cu.is_pressed(CosmicUnicorn.SWITCH_BRIGHTNESS_DOWN):
        cu.adjust_brightness(-0.1)
        update_display()

    refresh_display()


def initialise():
    print(f'Initialising...')
    cu.set_brightness(0.8)
    graphics.set_font('bitmap8')
    print(f'Restoring Matrix...')
    date_matrix.restore()
    print(f'Matrix Restored')
    update_display()
    print(f'Initialised')


def clear_display(background=BLACK):
    graphics.set_pen(background)
    graphics.clear()
    

def display_wifi(brightness=0.5, foreground=WHITE, background=BLACK):
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


if __name__ == "__main__":
    sync_time()
    initialise()
    while True:
        loop()
        time.sleep(0.01)
