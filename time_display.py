#!/usr/bin/env python3


zero = [
    0b111,
    0b101,
    0b101,
    0b101,
    0b111,
]

one = [
    0b110,
    0b010,
    0b010,
    0b010,
    0b111,
]

two = [
    0b111,
    0b001,
    0b111,
    0b100,
    0b111,
]

three = [
    0b111,
    0b001,
    0b111,
    0b001,
    0b111,
]

four = [
    0b101,
    0b101,
    0b111,
    0b001,
    0b001,
]

five = [
    0b111,
    0b100,
    0b111,
    0b001,
    0b111,
]

six = [
    0b111,
    0b100,
    0b111,
    0b101,
    0b111,
]

seven = [
    0b111,
    0b001,
    0b010,
    0b100,
    0b100,
]

eight = [
    0b111,
    0b101,
    0b111,
    0b101,
    0b111,
]

nine = [
    0b111,
    0b101,
    0b111,
    0b001,
    0b001,
]

colon = [
    0b000,
    0b100,
    0b000,
    0b100,
    0b000,
]

character_set = {0:zero, 1:one, 2:two, 3:three, 4:four, 5:five, 6:six, 7:seven, 8:eight, 9:nine, ':':colon}

def _draw_character(graphics, foreground, background, character, x_offset, y_offset):
    sprite = character_set[character]
    for y in range(len(sprite)):
        for x_idx, x in enumerate(reversed(range(4))):
            bit_set = (sprite[y] >> x) & 1 > 0
            print(f'x={x}, y={y}, set=0x{sprite[y]:02x}, bit_value={bit_set}')
            # bit_value = 1
            if bit_set :
                graphics.set_pen(foreground)
            else:
                graphics.set_pen(background)
            graphics.pixel(x_offset + x_idx, y_offset + y)


def split_digits(value):
    return int(value / 10), value % 10

def write_time(graphics, foreground, background, hour, minute, x_offset, y_offset):
    x = x_offset
    y = y_offset
    
    digit_one, digit_two = split_digits(hour)
    _draw_character(graphics, foreground, background, digit_one, x, y)
    x += 4
    _draw_character(graphics, foreground, background, digit_two, x, y)
    x += 4

    _draw_character(graphics, foreground, background, ':', x, y)
    x += 2

    digit_one, digit_two = split_digits(minute)
    _draw_character(graphics, foreground, background, digit_one, x, y)
    x += 4
    _draw_character(graphics, foreground, background, digit_two, x, y)
    x += 4
