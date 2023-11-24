#!/usr/bin/env python3

import time
from context import Context
from wifi import Wifi
from habit_calendar import HabitCalendar


class Controller:
    def __init__(self):
        self.context = Context()
        self.habit_calendar = HabitCalendar(self.context)

    def run(self):
        Wifi(self.context).sync_time()
        self.context.set_brightness(0.8);
        while True:
            self.loop()
            time.sleep(0.01)

    def loop(self):
        duration = self.context.process_button()
        if duration > 100:
            if duration < 1000:
                self.habit_calendar.button_pressed()
            else:
                print(f'Long push {duration}')

        self.habit_calendar.refresh_display()


if __name__ == "__main__":
    Controller().run()

