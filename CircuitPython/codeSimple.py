#------------------------------------------------------------------------------------------------------------------------
# Importing Libraries
#------------------------------------------------------------------------------------------------------------------------

import time, math
import board
import digitalio

#------------------------------------------------------------------------------------------------------------------------
# Defining Functions
#------------------------------------------------------------------------------------------------------------------------

# LDR Signal Callback; LDR == 0 when daytime, LDR == 1 when night time
def ldr_callback():
    global isDaytime
    if LDR_sense.value:
        isDaytime = False
        road_lights.value=True
    else:
        isDaytime = True
        road_lights.value=False

# Pedestrian Walk Signal Callback
def walk_callback():
    global isDaytime
    if (not walk_signal_2.value and not isDaytime) or (not walk_signal_4.value and not isDaytime):
        print("Button pressed")
        night_sequence()

# Car Signal Callback
def car_callback():
    global isDaytime
    # If car signals triggered during night, start night traffic light sequence
    if (not car_signal_2.value and not isDaytime) or (not car_signal_4.value and not isDaytime):
        print("Car detected")
        night_sequence()

# Function to run night time traffic sequence
def night_sequence():
    # Set Main Street traffic lights (No.2 and No.4) to yellow (STATE 1)
    G_Main_St.value=False
    Y_Main_St.value=True
    time.sleep(Y_timing)

    # Set Main Street light (No.2 and No.4) red, Small Avenue light (No.1 and No.3) green (STATE 2)
    Y_Main_St.value=False
    R_Main_St.value=True
    G_Small_Ave.value=True
    R_Small_Ave.value=False
    time.sleep(G_timing_night_Small_Ave)

    # Set Small Avenue (No.1 and No.3) traffic lights to yellow (STATE 3)
    G_Small_Ave.value=False
    Y_Small_Ave.value=True
    time.sleep(Y_timing)

    # Set Small Avenue light (No.1 and No.3) red, Main Street lights (No.2 and No.4) green (STATE 4)
    Y_Small_Ave.value=False
    R_Small_Ave.value=True
    R_Main_St.value=False
    G_Main_St.value=True

    # Wait 5 seconds before allowing traffic light change again
    time.sleep(5000)

# Function to run daytime traffic sequence
def day_sequence():
    # wait some time before changing the traffic lights
    time.sleep(G_timing_day_Main_St)

    # Set Main Street traffic lights (No.2 and No.4) to yellow (STATE 1)
    G_Main_St.value=False
    Y_Main_St.value=True
    time.sleep(Y_timing)

    # Set Main Street light (No.2 and No.4) red, Small Avenue light (No.1 and No.3) green (STATE 2)
    Y_Main_St.value=False
    R_Main_St.value=True
    G_Small_Ave.value=True
    R_Small_Ave.value=False
    time.sleep(G_timing_day_Small_Ave)

    # Set Small Avenue (No.1 and No.3) traffic lights to yellow (STATE 3)
    G_Small_Ave.value=False
    Y_Small_Ave.value=True
    time.sleep(Y_timing)

    # Set Small Avenue light (No.1 and No.3) red, Main Street lights (No.2 and No.4) green (STATE 4)
    Y_Small_Ave.value=False
    R_Small_Ave.value=True
    R_Main_St.value=False
    G_Main_St.value=True

# Function for pins
def Pin(pin, direction):
    p = digitalio.DigitalInOut(pin)
    p.direction = direction
    return p

#------------------------------------------------------------------------------------------------------------------------
# Initializations
#------------------------------------------------------------------------------------------------------------------------

# Road Lights
road_lights = Pin(board.GP0, digitalio.Direction.OUTPUT)

# Traffic Lights installed on corners "No.1" and "No.3"
G_Small_Ave = Pin(board.GP1, digitalio.Direction.OUTPUT)  # Green light
Y_Small_Ave = Pin(board.GP2, digitalio.Direction.OUTPUT)  # Yellow light
R_Small_Ave = Pin(board.GP3, digitalio.Direction.OUTPUT)  # Red light

# Traffic Lights installed on corners "No.2" and "No.4"
G_Main_St = Pin(board.GP4, digitalio.Direction.OUTPUT)  # Green light
Y_Main_St = Pin(board.GP5, digitalio.Direction.OUTPUT)  # Yellow light
R_Main_St = Pin(board.GP6, digitalio.Direction.OUTPUT)  # Red light

# Light Dependent Resistor (LDR)
LDR_sense = Pin(board.GP11, digitalio.Direction.INPUT)  # LDR signal pin

# Car and Walk Signals
car_signal_2 = Pin(board.GP7, digitalio.Direction.INPUT)   # Car signal on corner "No.2"
car_signal_4 = Pin(board.GP8, digitalio.Direction.INPUT)   # Car signal on corner "No.4"
walk_signal_2 = Pin(board.GP9, digitalio.Direction.INPUT)  # Pedestrian walk signal on corner "No.2"
walk_signal_4 = Pin(board.GP10, digitalio.Direction.INPUT) # Pedestrian walk signal on corner "No.4"

walk_signal_2.pull = digitalio.Pull.DOWN
walk_signal_4.pull = digitalio.Pull.DOWN

# Initializing street light states
G_Small_Ave.value=False
Y_Small_Ave.value=False
R_Small_Ave.value=True
G_Main_St.value=True
Y_Main_St.value=False
R_Main_St.value=False
road_lights.value=False

# Add a flag to check if it's daytime or not
isDaytime=False

# Adjust the day sequence traffic light timing here (milliseconds)
G_timing_night_Small_Ave = 5
G_timing_day_Small_Ave = 7
G_timing_day_Main_St = 15
Y_timing = 3


#------------------------------------------------------------------------------------------------------------------------
# Main Loop
#------------------------------------------------------------------------------------------------------------------------

while True:

    # check light, buttons and sensors
    ldr_callback()
    car_callback()
    walk_callback()

    if isDaytime:  #if it is daytime run the daytime traffic light sequence
        day_sequence()

    time.sleep(0.1)  # sleep for a while to reduce CPU usage (seconds)
