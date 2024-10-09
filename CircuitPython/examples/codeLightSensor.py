# Import libraries
import time, math
import board
import digitalio

# Setup street lights
street_light_pin = board.GP0
street_light = digitalio.DigitalInOut(street_light_pin)
street_light.direction = digitalio.Direction.OUTPUT

# Light Sensor
light_sensor_pin = board.GP11
light_sensor = digitalio.DigitalInOut(light_sensor_pin)
light_sensor.direction = digitalio.Direction.INPUT

# Turn street lights on and off

while True:
    street_light.value = light_sensor.value
    time.sleep(0.01)

