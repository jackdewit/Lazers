import RPi.GPIO as GPIO
import time
from stepperLib import setupStepper, homeStepper, moveStepper
import spidev
import numpy
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from GUI import setupGUI, clearScreen, graphPage, operationPage, statusPage

from ADCLib import setupADC, read_adc, plotReading

samples = 91
button_pin = 17

def main(): 
    try:
        
        #GUI Configuration
        disp, spi = setupGUI() #create display object
        image = Image.new("RGB", (disp.height, disp.width))
        draw = ImageDraw.Draw(image)
        clearScreen(disp)
        operationPage(draw, disp,image)
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(button_pin, GPIO.IN)

        spi = setupADC()
        
        setupStepper()
        pos = homeStepper()
            
        while 1:
            button_read = GPIO.input(button_pin)
            
            if button_read == 1:
                print('BEGINNING FOCUS')
                data = numpy.zeros(samples)
                
                for x in range(samples):
                    pos = moveStepper(pos, x)
                    data[x] = read_adc(0, spi)  
               
                bestFit = plotReading(data, samples)
                maximum = numpy.argmax(bestFit)
                pos = moveStepper(pos, maximum)
                      
                graphPage(disp, image)
                

    finally:
        GPIO.cleanup()
	spi.close()

if __name__ == '__main__':
    main()
