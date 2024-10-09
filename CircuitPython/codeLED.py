# Import libraries
import time, math
import board
import digitalio

# Setup street lights
street_light_pin = board.GP0
street_light = digitalio.DigitalInOut(street_light_pin)
street_light.direction = digitalio.Direction.OUTPUT

# Turn street lights on and off
street_light.value=True  # ON
time.sleep(1.0)
street_light.value=False  # OFF

