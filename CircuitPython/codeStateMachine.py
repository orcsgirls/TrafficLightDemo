#------------------------------------------------------------------------------------------------------------------------
# Importing Libraries
#------------------------------------------------------------------------------------------------------------------------

import time, math
import board
import digitalio

#-------------------------------------------------------------------------------------------------------------------------
# Function for pins
#-------------------------------------------------------------------------------------------------------------------------
def Pin(pin, direction):
    p = digitalio.DigitalInOut(pin)
    p.direction = direction
    return p

#-------------------------------------------------------------------------------------------------------------------------
# Traffic Light Class
#-------------------------------------------------------------------------------------------------------------------------
class TrafficLight:
    def __init__(self, G_pin, Y_pin, R_pin, initial_state='Red'):
        self.green_light = Pin(G_pin, digitalio.Direction.OUTPUT)        # Green light
        self.yellow_light = Pin(Y_pin, digitalio.Direction.OUTPUT)       # Yellow light
        self.red_light = Pin(R_pin, digitalio.Direction.OUTPUT)          # Red light

        self.state = initial_state
        self._update()

    def _update(self):
        if self.state == 'Red':
            self.red_light.value = True
            self.yellow_light.value = False
            self.green_light.value = False
        elif self.state == 'Yellow':
            self.red_light.value = False
            self.yellow_light.value = True
            self.green_light.value = False
        elif self.state == 'Green':
            self.red_light.value = False
            self.yellow_light.value = False
            self.green_light.value = True
        else:
            print(f"Invalid state {self.state}")

    def next(self):
        if self.state == 'Red':
            self.state = 'Green'
        elif self.state == 'Green':
            self.state = 'Yellow'
        elif self.state == 'Yellow':
            self.state = 'Red'
        self._update()

    def cycle(self):
        if self.state == 'Red':
            self.next()
        elif self.state == 'Green':
            self.next()
            time.sleep(0.7)
            self.next()

    def current_state(self):
        return self.state

#-------------------------------------------------------------------------------------------------------------------------
# Streelight Class
#-------------------------------------------------------------------------------------------------------------------------
class StreetLights:
    def __init__(self):
        self.light = Pin(board.GP0, digitalio.Direction.OUTPUT)
        self.sensor = Pin(board.GP11, digitalio.Direction.INPUT)
        self.state='auto'
        self.update()

    def update(self):
        if self.state=='off':
            self.light.value=False
        elif self.state=='on':
            self.light.value=True
        elif self.state=='auto':
            self.light.value=self.sensor.value

    def current_state(self):
        return self.state

#-------------------------------------------------------------------------------------------------------------------------'
# Buttons and car sensor class
#-------------------------------------------------------------------------------------------------------------------------'
class Sensors:
    def __init__(self):
        self.car_signal_2 = Pin(board.GP7, digitalio.Direction.INPUT)   # Car signal on corner "No.2"
        self.car_signal_4 = Pin(board.GP8, digitalio.Direction.INPUT)   # Car signal on corner "No.4"
        self.walk_signal_2 = Pin(board.GP9, digitalio.Direction.INPUT)  # Pedestrian walk signal on corner "No.2"
        self.walk_signal_4 = Pin(board.GP10, digitalio.Direction.INPUT) # Pedestrian walk signal on corner "No.4"#
        self.walk_signal_2.pull = digitalio.Pull.DOWN
        self.walk_signal_4.pull = digitalio.Pull.DOWN

    @property
    def car_waiting(self):
        return not self.car_signal_2.value or not self.car_signal_4.value

    @property
    def pedestrian_waiting(self):
        return not self.walk_signal_2.value or not self.walk_signal_4.value

    @property
    def triggered(self):
        return self.car_waiting or self.pedestrian_waiting
#-------------------------------------------------------------------------------------------------------------------------
# Intersection Class
#-------------------------------------------------------------------------------------------------------------------------
class Intersection:
    def __init__(self, light_main, light_side):
        self.light_main = light_main
        self.light_side = light_side
        self.state = 'Main'

    def change(self):
        if self.state == 'Main':
            self.light_main.cycle()
            time.sleep(0.5)
            self.light_side.cycle()
            self.state = 'Side'
        elif self.state == 'Side':
            self.light_side.cycle()
            time.sleep(0.5)
            self.light_main.cycle()
            self.state = 'Main'
        else:
            print(f"Invalid state {self.state}")

#-------------------------------------------------------------------------------------------------------------------------'
# Main Loop
#-------------------------------------------------------------------------------------------------------------------------'

# Traffic lights
side_street_light = TrafficLight(board.GP1, board.GP2, board.GP3, initial_state='Red')
main_street_light = TrafficLight(board.GP4, board.GP5, board.GP6, initial_state='Green')
street_lights = StreetLights()
side_street_sensors = Sensors()

intersection = Intersection(main_street_light, side_street_light)

while True:
    if intersection.state=='Main' and side_street_sensors.triggered:
        intersection.change()
        side_start=time.monotonic()

    if intersection.state=='Side' and (time.monotonic() - side_start > 10):
        intersection.change()

    street_lights.update()
    time.sleep(0.2)
