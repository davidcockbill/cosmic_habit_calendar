#!/usr/bin/env python3

import time
from context import Context
from wifi import Wifi
from habit_calendar import HabitCalendar

context = Context()
wifi = Wifi(context)
habit_calendar = HabitCalendar(context)

def loop():
    duration = context.process_button()
    if duration > 100:
        if duration < 1000:
            habit_calendar.button_pressed()
        else:
            print(f'Long push {duration}')

    habit_calendar.refresh_display()


if __name__ == "__main__":
    wifi.sync_time()
    context.set_brightness(0.8);
    while True:
        loop()
        time.sleep(0.01)
