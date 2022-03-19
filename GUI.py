import digitalio
import board
import datetime
import time
from PIL import Image, ImageDraw, ImageFont
from adafruit_rgb_display import ili9341

# Configuration for CS and DC pins (these are PiTFT defaults):
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = digitalio.DigitalInOut(board.D24)

# Config for display baudrate (default max is 24mhz):
BAUDRATE = 24000000

# Setup SPI bus using hardware SPI:
spi = board.SPI()

disp = ili9341.ILI9341(
    spi,
    rotation=270,  # 2.2", 2.4", 2.8", 3.2" ILI9341
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE,
)

# Create blank image for drawing.
image = Image.new("RGB", (disp.height, disp.width))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

def clearScreen():
    #Black Background
    # Draw a green filled box as the background
    draw.rectangle((0, 0, disp.height, disp.width), fill=(0, 0, 0))
    disp.image(image)

def statusPage(currentStatus, timeFocused):
    clearScreen()
    
    # Load a TTF Font
    FONTSIZE = 24
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", FONTSIZE)
    
    # Last Focused
    if currentStatus == 1:
        #Remove the microseconds to print to screen
        timeFocused = timeFocused.replace(microsecond = 0)
        
        # Draw Some Text
        text = f"Date of last focus:\n\n(YYYY-MM-DD HH:MM:SS)\n{timeFocused}\n\nReady for operation."
    
    # Focusing in progress
    if currentStatus == 2:
        text = "Focusing In Progress..."
    
    # Error status
    if currentStatus == 3:
        text = "Error"
        
    #Pint text to the screen
    draw.text(
        (0,0),
        text,
        font=font,
        fill=(255, 255, 255),
    )

    # Display image.
    disp.image(image)

def operationPage():
    FONTSIZE = 24
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", FONTSIZE)
    
    text = f"Stage Position: 10mm\nSensor 1 input: 0.100\nLimit switch status: 0"
    
    draw.text(
        (0,0),
        text,
        font=font,
        fill=(255, 255, 255),
    )
    
    disp.image(image)

    
def graphPage():
    image = Image.open("Figure_2.png")
    if disp.rotation % 180 == 90:
        height = disp.width  # we swap height/width to rotate it to landscape!
        width = disp.height
    else:
        width = disp.width  # we swap height/width to rotate it to landscape!
        height = disp.height

    # Scale the image to the smaller screen dimension
    image_ratio = image.width / image.height
    screen_ratio = width / height
    if screen_ratio < image_ratio:
        scaled_width = image.width * height // image.height
        scaled_height = height
    else:
        scaled_width = width
        scaled_height = image.height * width // image.width
    image = image.resize((scaled_width, scaled_height), Image.BICUBIC)

    # Crop and center the image
    x = scaled_width // 2 - width // 2
    y = scaled_height // 2 - height // 2
    image = image.crop((x, y, x + width, y + height))

    # Display image.
    disp.image(image)

def main():
    
    while 1:
        timeFocused = datetime.datetime.now()
        #statusPage(2,timeFocused)
        #time.sleep(20)
        operationPage()
        

if __name__ == '__main__':
    main()


    





