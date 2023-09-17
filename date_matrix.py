#!/usr/bin/env python3

import json

MAX_MONTH = 12
MAX_DAY = 31
DAYS_IN_MONTH = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]


def normalise_date(func):
    def wrapper(self, month, day):
        if month >= MAX_MONTH:
            print(f'Invalid month [month={month}. day={day}]')
        elif day >= DAYS_IN_MONTH[month]:
            print(f'Invalid day [month={month}. day={day}]')
        else:
            return func(self, month, day)
    return wrapper


class DateMatrix:
    def __init__(self):
        self.date_matrix = DateMatrix._blank_matrix()
        self.filename = 'matrix.json'

    @normalise_date
    def set(self, month, day):
        days = self.date_matrix[str(month)]
        self.date_matrix[str(month)] = days | (1 << day)

    @normalise_date
    def clear(self, month, day):
        days = self.date_matrix[str(month)]
        self.date_matrix[str(month)] = days & ~(1 << day)

    @normalise_date
    def toggle(self, month, day):
        print(f'toggle month={month}, day={day}')
        if self.isSet(month, day):
            self.clear(month, day)
        else:
            self.set(month, day)

    @normalise_date
    def isSet(self, month, day):
        return (self.date_matrix[str(month)] >> day & 1) != 0
    
    @staticmethod
    def month_range():
        return range(MAX_MONTH)
    
    @staticmethod
    def day_range(month):
        return range(DAYS_IN_MONTH[month])
    
    def store(self):
        with open(self.filename, 'w') as outfile:
            json.dump(self.date_matrix, outfile)

    def restore(self):
        try:
            with open(self.filename, 'r') as infile:
                self.date_matrix = json.load(infile)
        except OSError:
            pass

    @staticmethod
    def _blank_matrix():
        blank = {}
        for month in range(MAX_MONTH):
            blank[str(month)] = 0
        return blank
    

if __name__ == "__main__":
    date_matrix = DateMatrix()

    assert(date_matrix.isSet(0, 0) == False)
    assert(date_matrix.isSet(0, 1) == False)

    date_matrix.clear(0, 0)
    assert(date_matrix.isSet(0, 0) == False)
    assert(date_matrix.isSet(0, 1) == False)

    date_matrix.clear(0, 1)
    assert(date_matrix.isSet(0, 0) == False)
    assert(date_matrix.isSet(0, 1) == False)

    date_matrix.set(0, 0)
    assert(date_matrix.isSet(0, 0) == True)
    assert(date_matrix.isSet(0, 1) == False)

    date_matrix.set(0, 0)
    assert(date_matrix.isSet(0, 0) == True)
    assert(date_matrix.isSet(0, 1) == False)

    date_matrix.set(0, 1)
    assert(date_matrix.isSet(0, 0) == True)
    assert(date_matrix.isSet(0, 1) == True)

    date_matrix.clear(0, 0)
    assert(date_matrix.isSet(0, 0) == False)
    assert(date_matrix.isSet(0, 1) == True)
        
    date_matrix.clear(0, 1)
    assert(date_matrix.isSet(0, 0) == False)
    assert(date_matrix.isSet(0, 1) == False)

    date_matrix.toggle(0, 0)
    assert(date_matrix.isSet(0, 0) == True)
    assert(date_matrix.isSet(0, 1) == False)

    date_matrix.toggle(0, 1)
    assert(date_matrix.isSet(0, 0) == True)
    assert(date_matrix.isSet(0, 1) == True)

    date_matrix.toggle(0, 20)
    assert(date_matrix.isSet(0, 0) == True)
    assert(date_matrix.isSet(0, 1) == True)
    assert(date_matrix.isSet(0, 20) == True)