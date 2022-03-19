import time
import spidev
import numpy
import matplotlib.pyplot as plt
from ADCLib import setupADC, read_adc, plotReading

samples = 20

def main():
    data = numpy.zeros(samples)
    spi = setupADC()
        
    for x in range(samples):
        data[x] = read_adc(0, spi)
        time.sleep(0.25)
    
    print(numpy.argmax(data))
    plotReading(data, samples)

    spi.close()

if __name__ == '__main__':
    main()