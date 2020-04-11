# rpi_clock.py

import time
import RPi.GPIO as GPIO

# GPIO pin selection

data_pin = 17       # serial data sent over this pin
clock_pin = 27      # clock signal sent over this pin
latch_pin = 22      # latch signal sent over this pin

# GPIO setup

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(data_pin, GPIO.OUT)
GPIO.setup(clock_pin, GPIO.OUT)
GPIO.setup(latch_pin, GPIO.OUT)

# byre representations of each digit on a seven segment display

number = [
    0b11111100,     # zero
    0b01100000,     # one
    0b11011010,     # two
    0b11110010,     # three
    0b01100110,     # four
    0b10110110,     # five
    0b10111110,     # six
    0b11100000,     # seven
    0b11111110,     # eight
    0b11110110      # nine
]

# byte representations of each position on a four-digit display

digit = [
    0b00000000,     # blank
    0b10000000,     # first
    0b01000000,     # second
    0b00001000,     # third
    0b00000100      # fourth
]

# shift register interaction


def shift_out(data, data_pin, clock_pin):
    for _ in range(8):
        GPIO.output(data_pin, not not (data & (1 << _)))
        GPIO.output(clock_pin, True)
        GPIO.output(clock_pin, False)


# loop to multiplex current time to four-digit display

while True:
    current_time = int(time.strftime("%I%M"))

    if ((current_time // 1000) % 10) == 0:
        pass
    else:
        GPIO.output(latch_pin, False)
        shift_out(digit[1], data_pin, clock_pin)
        shift_out(number[(current_time // 1000) % 10], data_pin, clock_pin)
        GPIO.output(latch_pin, True)
    
    GPIO.output(latch_pin, False)
    shift_out(digit[2], data_pin, clock_pin)
    shift_out(number[(current_time // 100) % 10], data_pin, clock_pin)
    GPIO.output(latch_pin, True)

    GPIO.output(latch_pin, False)
    shift_out(digit[3], data_pin, clock_pin)
    shift_out(number[(current_time // 10) % 10], data_pin, clock_pin)
    GPIO.output(latch_pin, True)

    GPIO.output(latch_pin, False)
    shift_out(digit[4], data_pin, clock_pin)
    shift_out(number[current_time % 10], data_pin, clock_pin)
    GPIO.output(latch_pin, True)
