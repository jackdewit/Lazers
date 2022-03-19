import RPi.GPIO as GPIO
import time
from stepperLib import setupStepper, homeStepper, moveStepper
import spidev
import numpy
import matplotlib.pyplot as plt
from ADCLib import setupADC, read_adc, plotReading

samples = 20

def main():
    
    setupStepper()
    pos = homeStepper()
    
    data = numpy.zeros(samples)
    spi = setupADC()
        
    for x in range(samples):
        pos = moveStepper(pos, x)
        data[x] = read_adc(0, spi)
        time.sleep(0.5)
            
    maximum = numpy.argmax(data)
    
    pos = moveStepper(pos, maximum)
    
    plotReading(data, samples)
    
    GPIO.cleanup()
    spi.close()

if __name__ == '__main__':
    main()