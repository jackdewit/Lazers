import RPi.GPIO as GPIO
import time

step_pin = 5
dir_pin = 6 
home_pin = 13

def setupStepper():
    # Pin Setup:
    # Board pin-numbering scheme 
    GPIO.setmode(GPIO.BCM)

    # setup GPIO
    GPIO.setup(step_pin, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(dir_pin, GPIO.OUT, initial=GPIO.HIGH)
    GPIO.setup(home_pin, GPIO.IN)



def homeStepper():
    toggle = GPIO.HIGH
    GPIO.output(dir_pin, GPIO.LOW) #Set direction of stage towards motor (home)
    read = GPIO.input(home_pin) #Check if switch pressed
    
    while read == 1:
        time.sleep(0.001)
        GPIO.output(step_pin, toggle)
        toggle ^= GPIO.HIGH
        read = GPIO.input(home_pin)
	
    GPIO.output(dir_pin, GPIO.HIGH) #Reverse direction of stepper
    time.sleep(0.5)

    for x in range(200): #Move away from limit switch by 200 steps
        time.sleep(0.006)
        GPIO.output(step_pin, toggle)
        toggle ^= GPIO.HIGH
	
    GPIO.output(dir_pin, GPIO.LOW) #Back towards home	
    time.sleep(0.5)
    read = GPIO.input(home_pin)

    while read == 1: #Rehome stage
        time.sleep(0.006)
        GPIO.output(step_pin, toggle)
        toggle ^= GPIO.HIGH
        read = GPIO.input(home_pin)
        
    #Set position to zero - home
    return 0.00



def moveStepper(position, setpoint):
    toggle = GPIO.HIGH
    #2mm per full rotation, 200 pulses per full rotation - 0.01 mm/pulse        
            
    #Set required direction of stage to get to setpoint
    if (float(setpoint) - position) < 0:
        GPIO.output(dir_pin, GPIO.LOW)
        direction = "reverse"
    else:
        GPIO.output(dir_pin, GPIO.HIGH)
        direction = "forward"
            
            #Move to specified position
    while abs(float(setpoint) - position) > 0.02:
        time.sleep(0.003)
        GPIO.output(step_pin, toggle)
        toggle ^= GPIO.HIGH

        if direction == "forward":
            position = position + 0.02
        else:
            position = position - 0.02

    return position