#!/usr/bin/env python3

from date_matrix import DateMatrix
from time_display import write_time


MONTHS = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']


class HabitCalendar:
    def __init__(self, context):
        self.context = context
        self.date_matrix = DateMatrix()
        self.last_refresh_minute = int(0)

        self.restore_matrix()
        self.update_display()

    def restore_matrix(self):
        print(f'Restoring Matrix...')
        self.date_matrix.restore()
        print(f'Matrix Restored')

    def button_pressed(self):
        self.toggle_day()

    def toggle_day(self):
        month, day = self.current_date()
        print(f'Setting month={month}, day={day}')
        self.date_matrix.toggle(month-1, day-1)
        self.date_matrix.store()
        self.display_date_matrix()

    def update_display(self):
        self.context.clear_display(self.background())
        self.display_date()
        self.display_time()
        self.display_date_matrix()
        self.context.update_display()

    def display_date(self):
        month, day = self.current_date()
        date = f'{MONTHS[month-1]} {day:02}'

        self.context.set_pen(self.context.orange())
        self.context.graphics.text(date, 3, 2, scale=1, spacing=1)

    def display_time(self):
        _, _, _, _, hour, minute, _, _ = self.context.datetime()
        write_time(self.context.graphics, self.context.dark_green(), self.background(), hour, minute, 7, 11)
        self.last_refresh_minute = minute

    def current_date(self):
        _, month, day, _, _, _, _, _ = self.context.datetime()
        return month, day

    def display_date_matrix(self):
        current_month, current_day = self.current_date()
        row = 18

        # Top Border
        self.context.set_pen(self.matrix_border())
        self.context.graphics.line(0, row, 32, row)
        row += 1

        # Matrix
        for month in DateMatrix.month_range():
            self.context.set_pen(self.off())
            self.context.graphics.line(0, row, 32, row)
            for day in DateMatrix.day_range(month):
                today = day == current_day-1 and month == current_month-1
                column = day
                pen = self.today_off() if today else self.off()
                if (self.date_matrix.isSet(month, day)):
                    pen = self.today_on() if today else self.on()
                self.context.set_pen(pen)
                self.context.graphics.pixel(column, row)

            row += 1

        # Bottom Border 
        self.context.set_pen(self.matrix_border())
        self.context.graphics.line(0, row, 32, row)

        self.context.update_display()

    def refresh_display(self):
        _, _, _, _, _, current_minute, _, _ = self.context.datetime()
        if current_minute != self.last_refresh_minute:
            self.update_display()

    def on(self):
        return self.context.blue()
        
    def off(self):
        return self.context.light_grey()
        
    def today_on(self):
        return self.context.green()
        
    def today_off(self):
        return self.context.pink()
        
    def matrix_border(self):
        return self.context.dark_blue()

    def background(self):
        return self.context.dark_background_blue()
