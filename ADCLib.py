import time
import spidev
import numpy
import matplotlib.pyplot as plt

spi_ch = 1

# Enable SPI
def setupADC():
    spi = spidev.SpiDev(0, spi_ch) 
    spi.max_speed_hz = 1200000
    return spi


def read_adc(adc_ch, spi, vref = 3.1):

    # Make sure ADC channel is 0 or 1
    if adc_ch != 0: print("Error. Please select ADC Channel 0.")
    
    # Construct SPI message
    # Byte 1:
    # Five leading zeroes
    # 1 - Start bit
    # 1 - Single mode
    # 0 - Next three bits select channel
    # Byte 2
    # 0 - Still channel bits
    # 0 - Still channel bits
    # Rest don't care, all zeroes
    # Byte 3
    # Don't care, all zeroes
    
    reply = spi.xfer2([0b00000110, 0b00000000, 0b00000000])
        
    # Construct single integer out of the reply (3 bytes)
    # First byte received is garbage data
    # Last four bits of second byte are MSBs
    # Third byte contains last eight bits of twelve bit response
    adc = 0
    adc = ((reply[1]&0b00001111) << 8) + reply[2]

    # Calculate voltage form ADC value
    voltage = (vref * adc) / 4096 
    
    return voltage


def plotReading(data, samples):
    X_axis = numpy.linspace(1, samples, samples)

    #Determine coefficients of quadratic line of best fit
    bestFit = numpy.polyfit(X_axis, data, 2)
    
    #Create line of best fit
    y = numpy.zeros(samples)
    
    for x in range(samples):
        y[x] = bestFit[0]*x*x+bestFit[1]*x+bestFit[2]
    
    #Plot ADC data and line of best fit
    plt.figure()
    plt.plot(X_axis, data, linewidth=3, label='ADC Data')
    plt.plot(X_axis, y, linewidth=3, label='Best Fit')
    plt.legend()
    plt.savefig('data.jpg')
    #plt.show()
    
    return y
    
def main():
    spi = setupADC()
    while 1:
        read =read_adc(0, spi)
        print(read)
        time.sleep(0.5)
    
if __name__ == '__main__':
    main()
