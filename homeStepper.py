import RPi.GPIO as GPIO
import time

# Pin Definitions
step_pin = 24  # BOARD pin 12, BCM pin 18
dir_pin = 10 # BOARD pin 16, BCM pin 16
home_pin = 9

def main():
    # Pin Setup:
    # Board pin-numbering scheme
    GPIO.setmode(GPIO.BCM)

    # setup GPIO
    GPIO.setup(step_pin, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(dir_pin, GPIO.OUT, initial=GPIO.HIGH)
    GPIO.setup(home_pin, GPIO.IN)

    print("Starting demo now! Press CTRL+C to exit")
    toggle = GPIO.HIGH
    GPIO.output(dir_pin, GPIO.LOW) #Set direction of stage towards motor (home)
    read = GPIO.input(home_pin) #Check if switch pressed

    try:
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

    finally:
        GPIO.cleanup()

if __name__ == '__main__':
    main()
