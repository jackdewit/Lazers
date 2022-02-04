import time
import spidev
import numpy
from ADC import read_adc
import matplotlib.pyplot as plt

spi_ch = 0

# Enable SPI
spi = spidev.SpiDev(0, spi_ch)
spi.max_speed_hz = 1200000

def read_adc(adc_ch, vref = 5):

    # Make sure ADC channel is 0 or 1
    if adc_ch != 0: print("Error. Please select ADC Channel 0.")
    # Construct SPI message
    #  First bit (Start): Logic high (1)
    #  Second bit (SGL/DIFF): 1 to select single mode
    #  Third bit (ODD/SIGN): Select channel (0 or 1)
    #  Fourth bit (MSFB): 0 for LSB first
    #  Next 12 bits: 0 (don't care)
    msg = 0b11
    msg = ((msg << 1) + adc_ch) << 5
    msg = [msg, 0b00000000]
    reply = spi.xfer2(msg)

    # Construct single integer out of the reply (2 bytes)
    adc = 0
    for n in reply:
        adc = (adc << 8) + n
  
     # Last bit (0) is not part of ADC value, shift to remove it
    adc = adc >> 1

    # Calculate voltage form ADC value
    voltage = (vref * adc) / 4096

    return voltage

#Reads ADC channel over interval [seconds] taking n measurements
def intervalScan(interval, n, channel):
    
    f = interval/n #Calculate sampling frequency

    array = numpy.zeros(n)
    
    for j in range(n):
        array[j] = read_adc(channel)
        time.sleep(f)
        
    return array

try:
    
    array = intervalScan(10, 50, 0)
    X_axis = numpy.linspace(1,50)

    #Determine coefficients of quadratic line of best fit
    bestFit = numpy.polyfit(X_axis, array, 2)
    
    #Create line of best fit
    y = numpy.zeros(50)
    
    for x in range(50):
        y[x] = bestFit[0]*x*x+bestFit[1]*x+bestFit[2]
    
    #Plot ADC data and line of best fit
    plt.figure()
    plt.plot(X_axis, array, label='ADC Data')
    plt.plot(X_axis, y, label='Best Fit')
    plt.legend()
    plt.show()
    
finally:

    spi.close()
