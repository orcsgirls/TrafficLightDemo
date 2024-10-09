# Import libraries
import time, math
import board
import digitalio

# Setup street lights
street_light_pin = board.GP0
street_light = digitalio.DigitalInOut(street_light_pin)
street_light.direction = digitalio.Direction.OUTPUT

# Walk button
button_pin = board.GP9
button = digitalio.DigitalInOut(button_pin)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.DOWN

# Turn street lights on and off
while True:
    street_light.value = button.value
    time.sleep(0.5)

