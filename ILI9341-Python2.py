# ILI9341 driver in python
# By Bob Davis
# Adapted from code on the Internet
 
import RPi.GPIO as GPIO
import spidev           
import time
import sys

RS=23   # Data/Control Ao
RST=24  # Reset
SCE=8   # CS
SCLK=11 # SCLK Clock
DIN=10  # SDA MOSI
spi = spidev.SpiDev()

# MCP3008 ALTERNATE lines
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT) # Replaces CE0
GPIO.setup(18, GPIO.IN)  # Replaces MISO
GPIO.setup(27, GPIO.OUT) # Replaces MOSI 
GPIO.setup(22, GPIO.OUT) # Replaces Sclock

font = {  # Reduced Character Set
  ' ': [0x00, 0x00, 0x00, 0x00, 0x00],
  '/': [0x20, 0x10, 0x08, 0x04, 0x02],
  '0': [0x3e, 0x51, 0x49, 0x45, 0x3e],
  '1': [0x00, 0x42, 0x7f, 0x40, 0x00],
  '2': [0x42, 0x61, 0x51, 0x49, 0x46],
  '3': [0x21, 0x41, 0x45, 0x4b, 0x31],
  '4': [0x18, 0x14, 0x12, 0x7f, 0x10],
  '5': [0x27, 0x45, 0x45, 0x45, 0x39],
  '6': [0x3c, 0x4a, 0x49, 0x49, 0x30],
  '7': [0x01, 0x71, 0x09, 0x05, 0x03],
  '8': [0x36, 0x49, 0x49, 0x49, 0x36],
  '9': [0x06, 0x49, 0x49, 0x29, 0x1e],
  ':': [0x00, 0x36, 0x36, 0x00, 0x00],
  '=': [0x14, 0x14, 0x14, 0x14, 0x14],
  'A': [0x7e, 0x11, 0x11, 0x11, 0x7e],
  'B': [0x7f, 0x49, 0x49, 0x49, 0x36],
  'C': [0x3e, 0x41, 0x41, 0x41, 0x22],
  'D': [0x7f, 0x41, 0x41, 0x22, 0x1c],
  'E': [0x7f, 0x49, 0x49, 0x49, 0x41],
  'F': [0x7f, 0x09, 0x09, 0x09, 0x01],
  'G': [0x3e, 0x41, 0x49, 0x49, 0x7a],
  'H': [0x7f, 0x08, 0x08, 0x08, 0x7f],
  'I': [0x00, 0x41, 0x7f, 0x41, 0x00],
  'J': [0x20, 0x40, 0x41, 0x3f, 0x01],
  'K': [0x7f, 0x08, 0x14, 0x22, 0x41],
  'L': [0x7f, 0x40, 0x40, 0x40, 0x40],
  'M': [0x7f, 0x02, 0x0c, 0x02, 0x7f],
  'N': [0x7f, 0x04, 0x08, 0x10, 0x7f],
  'O': [0x3e, 0x41, 0x41, 0x41, 0x3e],
  'P': [0x7f, 0x09, 0x09, 0x09, 0x06],
  'Q': [0x3e, 0x41, 0x51, 0x21, 0x5e],
  'R': [0x7f, 0x09, 0x19, 0x29, 0x46],
  'S': [0x46, 0x49, 0x49, 0x49, 0x31],
  'T': [0x01, 0x01, 0x7f, 0x01, 0x01],
  'U': [0x3f, 0x40, 0x40, 0x40, 0x3f],
  'V': [0x1f, 0x20, 0x40, 0x20, 0x1f],
  'W': [0x3f, 0x40, 0x38, 0x40, 0x3f],
  'X': [0x63, 0x14, 0x08, 0x14, 0x63],
  'Y': [0x07, 0x08, 0x70, 0x08, 0x07],
  'Z': [0x61, 0x51, 0x49, 0x45, 0x43],
  '\\': [0x02, 0x04, 0x08, 0x10, 0x20],
}
 
def init():
  spi.open(0, 0)
  spi.max_speed_hz = 60000000  # Maximum safe speed.
  GPIO.setmode(GPIO.BCM)
#  GPIO.setwarnings ( False )
  GPIO.setup (RS, GPIO.OUT)
  GPIO.setup (RST, GPIO.OUT)
  Reset()
  Write_cmd ( 0X11 )
  time.sleep ( 0.12 )
# RPI ILI9340 driver
  Write_CD((0xCF, 0x00, 0X83, 0X30))
  Write_CD((0xED, 0x64, 0x03, 0X12, 0X81) )
  Write_CD((0xE8, 0x85, 0x01, 0x79)) 
  Write_CD((0xCB, 0x39, 0x2C, 0x00, 0x34, 0x02) )
  Write_CD((0xF7, 0x20)) 
  Write_CD((0xEA, 0x00, 0x00)) 
  Write_CD((0xC0, 0x26)) # Power control 
  Write_CD((0xC1, 0x11)) # Power control 
  Write_CD((0xC5, 0x35, 0x3e)) # VCM control 
  Write_CD((0xC7, 0xbe)) # VCM control2 
  Write_CD((0x36, 0x48)) # 40=RGB Memory Access Control 
  Write_CD((0x3A, 0x06)) # Sequential r,g,b bytes 
  Write_CD((0xB1, 0x00, 0x1b)) 
  Write_CD((0xB6, 0x0a, 0x82, 0x27, 0x00))# Display Control 
  Write_CD((0xF2, 0x00)) # 3Gamma Function Disable 
  Write_CD((0x26, 0x01)) # Gamma curve selected 
  Write_CD((0xE0, 0x0F, 0x31, 0x2B, 0x0C, 0x0E, 0x08, 0x4E, 0xF1, 0x37, 0x07, 0x10, 0x03, 0x0E, 0x09, 0x00)) 
  Write_CD((0xE1, 0x00, 0x0E, 0x14, 0x03, 0x11, 0x07, 0x31, 0xC1, 0x48, 0x08, 0x0F, 0x0C, 0x31, 0x36, 0x0F)) 
  Write_cmd(0x29)      # Display on 
  Write_CD (( 0X2A, 0X00, 0X00, 0X00, 0XEf )) #240 Columns
  Write_CD (( 0X2B, 0X00, 0X00, 0X01, 0X3F )) #320 rows
  Write_cmd ( 0X2C ) # Next: red, Green, Blue bytes

def Reset (): # Reset Display
  GPIO.output (RST, False )
  time.sleep ( 0.1 )
  GPIO.output (RST, True )
  time.sleep ( 0.1 )
def Write_cmd (cmd): # Write Command
  GPIO.output (RS, False )  # RS = 0
  spi.writebytes([cmd])
def Write_data (Data): # Write data
  GPIO.output (RS, True )   # RS = 1
  spi.writebytes([Data])
def Write_CD (cmd): #Write command followed by data
  if len (cmd) == 0 :
    return
  GPIO.output (RS, False ) # RS = 0
  spi.writebytes ([cmd [ 0 ]])
  GPIO.output (RS, True )  # RS = 1
  spi.writebytes ( list (cmd [ 1 :]))

def Fill (red, green, blue):
  pixline = []
  for n in range (0,320): # Fill screen with white
    if (blue==1):pixline.append (0xff) # Blue       
    else :pixline.append (0x00) # Blue       
    if (green==1):pixline.append (0xff) # Green
    else :pixline.append (0x00) # Green
    if (red==1):pixline.append (0xff) # RED
    else: pixline.append (0x00) # RED
  for n in range (240):   # send data to LCD
    spi.writebytes (pixline [ 0 :])
    
def goto (x, y):  # go to x y coordinates
  if (y>255): # Fix for numbers over 255
    Y = y-256
    Write_CD (( 0X2A, 0X00, x, 0X00, 0XEf )) #240 Columns
    Write_CD (( 0X2B, 1, y, 0X01, 0X3F )) #320 rows
  else:
    Write_CD (( 0X2A, 0X00, x, 0X00, 0XEf )) #240 Columns
    Write_CD (( 0X2B, 0X00, y, 0X01, 0X3F )) #320 rows
  Write_cmd ( 0X2C ) # Next: red, Green, Blue bytes
  GPIO.output (RS, True )  # RS = 1 will send data
  
def Image (filename):
  try:  # Prevents crashing when images do not work
    with open(filename, 'rb') as bitmap: # Must be 128x128 image
      for x in range ( 0,320 ):
        pixline = []
        for y in range ( 0,720 ):
          bitmap.seek(0x36 + x*720 + (719-y)) # 36 is header size
          Pixel = ord(bitmap.read(1)) # 719-y reverse image horizontally
          pixline.append (Pixel)
        spi.writebytes (pixline)
  except:
      pass
    
def text(string, red, green, blue):
  if (red==1):red=255
  if (green==1):green=255
  if (blue==1):blue=255
  string=string.ljust(40, " ") # 240/6=40 characters
  for row in range(0,10): # 10 rows top to bottom
    pixline = []
    for char in string: # Procees each character in string
      for byte in range(0,5):
        data=(font[char])  # Load 5 bytes of character
        pix=0
        if (row<8):
          if(data[byte]>>row & 0x01):pix=1
        if (row>7):pix=0  # Blank between lines
        if (pix==1):       # fill in R/G/B
          pixline.append (blue)
          pixline.append (green)
          pixline.append (red)
        else:   
          pixline.append (0x00)
          pixline.append (0x00)
          pixline.append (0x00)
      pixline.append (0x00) # blanks between characters
      pixline.append (0x00)
      pixline.append (0x00)
    spi.writebytes(pixline)
    pixline = []

def dtext(string, red, green, blue): # double size text
  if (red==1):red=255
  if (green==1):green=255
  if (blue==1):blue=255
  string=string.ljust(20, " ") # 240/6=40 characters
  for row in range(0,20): # 20 rows top to bottom
    pixline = []
    for char in string: # Procees each character in string
      for byte in range(0,5):
        data=(font[char])  # Load 5 bytes of character
        pix=0
        if (row<17):
          if(data[byte]>>(row/2) & 0x01):pix=1
        if (row>16):pix=0  # Blank between lines
        for twice in range(0,2):
          if (pix==1):       # fill in R/G/B
            pixline.append (blue)
            pixline.append (green)
            pixline.append (red)
          else:   
            pixline.append (0x00)
            pixline.append (0x00)
            pixline.append (0x00)
      for i in range(0,6):
        pixline.append (0x00) # blanks between characters
    spi.writebytes(pixline)
    pixline = []

def readport(port): # Alternate pins
  GPIO.output(17, GPIO.HIGH) # deselect chip
  GPIO.output(22, GPIO.LOW) # set clock low
  adcin=0
  for shift in range (0,24): # 24 pits shifted
    GPIO.output(17, GPIO.LOW) # select chip
    GPIO.output(27, GPIO.LOW) # low for most bits
    if (shift==7 or shift==8): 
      GPIO.output(27, GPIO.HIGH)
    if (shift==9)and(port & 0x04): 
      GPIO.output(27, GPIO.HIGH)
    if (shift==10)and(port & 0x02): 
      GPIO.output(27, GPIO.HIGH)
    if (shift==11)and(port & 0x01): 
      GPIO.output(27, GPIO.HIGH)
    if (shift > 13)and(GPIO.input(18)):
      adcin = adcin+1 # set bit
    adcin = adcin << 1  # left shift 1
    GPIO.output(22, GPIO.LOW) # cycle the clock
    GPIO.output(22, GPIO.HIGH) 
  return (adcin)  

def sketch():
  for y in range(0,10000):
    pixline=[]
    analogx=(readport(0)/4)
    analogy=(readport(1)/3)
    analogr=(readport(5)/4)
    analogg=(readport(6)/4)
    analogb=(readport(7)/4)
    goto (analogx, analogy)
    # Next: RGB bytes
    pixline.append (analogr)
    pixline.append (analogg)
    pixline.append (analogb)
    spi.writebytes(pixline)
  time.sleep(.01)
 
if __name__ == "__main__" :
  init ()
  T1 = time.clock ()
  goto (0, 64)
  Fill (1,0,0) # Blue
  goto (0, 128)
  Fill (0,1,0) # Green
  goto (0, 192)
  Fill (0,0,1) # Red
  goto (0, 256)
  Fill (1,1,1) # white
  time.sleep(2)
  goto(0,0)
  Image ("RPI-240.bmp")
  time.sleep(2)
  goto(0,0)
  Image ("Parrots-240.bmp")
  time.sleep(2)
  Fill (0,0,0) # black
  sketch()
  time.sleep(2)
  goto(0,0)
  Fill (0,0,0) # black
  #Convert time and date to strings
  times=time.strftime('%H:%M:%S')
  dates=time.strftime('%D')
  # Read analog ports
  analog1=(readport(0))  # Range 0-1024 
  analog2=(readport(1))
  analog3=(readport(2))   
  analog4=(readport(3))
  analog5=(readport(4))   
  analog6=(readport(5))
  analog7=(readport(6))   
  analog8=(readport(7))
  text("THIS IS A TEST OF THE 320X240 LCD", 1,0,0) # Blue
  text("WRITTEN BY ROBERT J DAVIS II", 0,1,0)  # green
  text("THE CURRENT DATE AND TIME IS:", 0,0,1) # RED
  text(times+" "+dates, 1,1,1)    # white
  dtext ("IN BIGGER LETTERS:", 1,0,1) 
  dtext(times+" "+dates, 1,1,1)    # white
  text("ANALOG 1 IS "+str(analog1),1,1,1)
  text("ANALOG 2 IS "+str(analog2),1,1,0)
  text("ANALOG 3 IS "+str(analog3),0,1,1)
  text("ANALOG 4 IS "+str(analog4),1,0,1)
  text("ANALOG 5 IS "+str(analog5),1,1,1)
  text("ANALOG 6 IS "+str(analog6),1,1,0)
  text("ANALOG 7 IS "+str(analog7),0,1,1)
  text("ANALOG 8 IS "+str(analog8),1,0,1)
  T2 = time.clock ()
  print 'Processing Time:' , str (T2 - T1)
