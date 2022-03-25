import RPi.GPIO as GPIO
import time
from stepperLib import setupStepper, homeStepper, moveStepper
import spidev
import numpy
from PIL import Image, ImageDraw, ImageFont
from GUI import setupGUI, clearScreen, graphPage, operationPage, statusPage

from ADCLib import setupADC, read_adc, plotReading

samples = 60
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
        
        setupStepper()
        pos = homeStepper()
            
        while 1:
            button_read = GPIO.input(button_pin)
            print(button_read)
            
            if button_read == 1:
                print('BEGINNING FOCUS')
                data = numpy.zeros(samples)
                spi = setupADC()
                
                for x in range(samples):
                    pos = moveStepper(pos, x)
                    data[x] = read_adc(0, spi)
                    time.sleep(0.2)   
                
                maximum = numpy.argmax(data)
                print(maximum)
            
                pos = moveStepper(pos, maximum)
            
                print(numpy.argmax(data))
                plotReading(data, samples)
                graphPage(disp, image)
                spi.close()

    finally:
        GPIO.cleanup()

if __name__ == '__main__':
    main()
