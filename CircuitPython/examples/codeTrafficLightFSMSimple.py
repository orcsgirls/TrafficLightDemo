# Import libraries
import time, math
import board
import digitalio

# Traffic light FSM
class TrafficLight():
    def __init__(self, red, yellow, green, initial_state='Red'):
        self.red=red
        self.yellow=yellow
        self.green=green
        self.state = initial_state
        self.setState()
        
    def setState(self):
        if self.state == 'Red':
            self.red.value = True
            self.yellow.value = False
            self.green.value = False
        elif self.state == 'Yellow':
            self.red.value = False
            self.yellow.value = True
            self.green.value = False
        elif self.state == 'Green':
            self.red.value = False
            self.yellow.value = False
            self.green.value = True
        else:
            print(f"Invalid state {self.state}")
            
    def cycle(self):
        if self.state == 'Red':
            time.sleep(2)
            self.state = 'Green'
        elif self.state == 'Green':
            time.sleep(2)
            self.state = 'Yellow'
        elif self.state == 'Yellow':
            time.sleep(0.5)
            self.state = 'Red'
            
        self.setState()
            
    def current_state(self):
        return self.state
#------------------------------------------------------------------------------  
# Initialize all the LEDs
red = digitalio.DigitalInOut(board.GP3)
red.direction = digitalio.Direction.OUTPUT
yellow = digitalio.DigitalInOut(board.GP2)
yellow.direction = digitalio.Direction.OUTPUT
green = digitalio.DigitalInOut(board.GP1)
green.direction = digitalio.Direction.OUTPUT

# Create traffic light
traffic_light = TrafficLight(red, yellow, green)

while True:
    traffic_light.cycle()
    print(traffic_light.current_state())


