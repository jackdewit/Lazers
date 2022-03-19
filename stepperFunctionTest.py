import RPi.GPIO as GPIO
import time
from stepperLib import setupStepper, homeStepper, moveStepper

def main(): 
    try:
        
        setupStepper()
        pos = homeStepper()
        
        print("Press CTRL+C to exit")
        
        while 1:
            #Now take user input to move to specific position
            target = input("Enter position in mm: ")
            
            print("Moving to ", target, "mm")
            pos = moveStepper(pos, target)
            print("Final position: ", pos)   
            

    finally:
        GPIO.cleanup()

if __name__ == '__main__':
    main()