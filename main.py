#!/usr/bin/env python3

import time
from context import Context
from wifi import Wifi
from habit_calendar import HabitCalendar
from fire import Fire
from brightness import Brightness


class Controller:
    def __init__(self):
        self.context = Context()
        self.page_idx = 0
        self.page = [
            HabitCalendar(self.context),
            Fire(self.context),
            Brightness(self.context),
        ]
        
    def run(self):
        Wifi(self.context).sync_time()
        self.context.clear_display()
        while True:
            self._loop()
            time.sleep(0.001)

    def _loop(self):
        duration = self.context.process_button()
        if duration > 100:
            if duration < 1000:
                self._current_page().button_pressed()
            else:
                print(f'Long push {duration}')
                self._increment_page()

        self._current_page().refresh_display()

    def _current_page(self):
        return self.page[self.page_idx]
    
    def _increment_page(self):
        self.page_idx = (self.page_idx + 1) % len(self.page)
        self._current_page().enter()


if __name__ == "__main__":
    Controller().run()

