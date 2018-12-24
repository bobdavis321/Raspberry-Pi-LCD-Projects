# ILI9325 PARALLEL driver in python
# By Bob Davis
# Adapted from code on the Internet
 
import RPi.GPIO as GPIO
import time
import sys
# dATA lines
D0=17
D1=18
D2=27
D3=22
D4=23
D5=24
D6=25
D7=4
# cOMMAND Lines
RS=3   # Data/Control 
RST=15 # Reset
CS=7   # Chip Select
WR=2   # Write clock
# MCP3008 lines
GPIO.setmode(GPIO.BCM)
GPIO.setup(8, GPIO.OUT)  # CE0
GPIO.setup(9, GPIO.IN)   # MISO
GPIO.setup(10, GPIO.OUT) # MOSI 
GPIO.setup(11, GPIO.OUT) # Sclock

font = { #reduced set
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
  '[': [0x00, 0x7f, 0x41, 0x41, 0x00],
  '\\': [0x02, 0x04, 0x08, 0x10, 0x20],
}
 
def init():
  GPIO.setup (D0, GPIO.OUT)
  GPIO.setup (D1, GPIO.OUT)
  GPIO.setup (D2, GPIO.OUT)
  GPIO.setup (D3, GPIO.OUT)
  GPIO.setup (D4, GPIO.OUT)
  GPIO.setup (D5, GPIO.OUT)
  GPIO.setup (D6, GPIO.OUT)
  GPIO.setup (D7, GPIO.OUT)
  GPIO.setup (RS, GPIO.OUT)
  GPIO.setup (RST, GPIO.OUT)
  GPIO.setup (CS, GPIO.OUT)
  GPIO.setup (WR, GPIO.OUT)
  Reset()

# set up for ILI9325D:
  WriteCD(0xE5, 0x78, 0xF0); # set SRAM internal timing
  WriteCD(0x01, 0x01, 0x00); # set Driver Output Control  
  WriteCD(0x02, 0x02, 0x00); # set 1 line inversion  
  WriteCD(0x03, 0xC0, 0x30); # D0=Set 3 bytes per color BGR=1.  
  WriteCD(0x04, 0x00, 0x00); # Resize register  
  WriteCD(0x08, 0x02, 0x07); # set the back porch and front porch  
  WriteCD(0x09, 0x00, 0x00); # set non-display area refresh cycle ISC[3:0]  
  WriteCD(0x0A, 0x00, 0x00); # FMARK function  
  WriteCD(0x0C, 0x00, 0x00); # RGB interface setting  
  WriteCD(0x0D, 0x00, 0x00); # Frame marker Position  
  WriteCD(0x0F, 0x00, 0x00); # RGB interface polarity  
  WriteCD(0x10, 0x00, 0x00); # SAP, BT[3:0], AP, DSTB, SLP, STB  
  WriteCD(0x11, 0x00, 0x07); # DC1[2:0], DC0[2:0], VC[2:0]  
  WriteCD(0x12, 0x00, 0x00); # VREG1OUT voltage  
  WriteCD(0x13, 0x00, 0x00); # VDV[4:0] for VCOM amplitude  
  WriteCD(0x07, 0x00, 0x01);  
  time.sleep ( 0.00001 )
  WriteCD(0x10, 0x16, 0x90); # SAP, BT[3:0], AP, DSTB, SLP, STB  
  WriteCD(0x11, 0x02, 0x27); # Set DC1[2:0], DC0[2:0], VC[2:0]  
  time.sleep ( 0.00001 )
  WriteCD(0x12, 0x00, 0x0D); # 0012  
  time.sleep ( 0.00001 )
  WriteCD(0x13, 0x12, 0x00); # VDV[4:0] for VCOM amplitude  
  WriteCD(0x29, 0x00, 0x0A); # 04  VCM[5:0] for VCOMH  
  WriteCD(0x2B, 0x00, 0x0D); # Set Frame Rate  
  time.sleep ( 0.00001 )
  WriteCD(0x20, 0x00, 0x00); # GRAM horizontal Address  
  WriteCD(0x21, 0x00, 0x00); # GRAM Vertical Address  
  WriteCD(0x30, 0x00, 0x00); # Gamma Curve  
  WriteCD(0x31, 0x04, 0x04);  
  WriteCD(0x32, 0x00, 0x03);  
  WriteCD(0x35, 0x04, 0x05);  
  WriteCD(0x36, 0x08, 0x08);  
  WriteCD(0x37, 0x04, 0x07);  
  WriteCD(0x38, 0x03, 0x03);  
  WriteCD(0x39, 0x07, 0x07);  
  WriteCD(0x3C, 0x05, 0x04);  
  WriteCD(0x3D, 0x08, 0x08);  
  #------------------ Set GRAM area ---------------#  
  WriteCD(0x50, 0x00, 0x00); # Horizontal GRAM Start Address  
  WriteCD(0x51, 0x00, 0xEF); # Horizontal GRAM End Address  
  WriteCD(0x52, 0x00, 0x00); # Vertical GRAM Start Address  
  WriteCD(0x53, 0x01, 0x3F); # Vertical GRAM Start Address  
  WriteCD(0x60, 0xA7, 0x00); # Gate Scan Line  
  WriteCD(0x61, 0x00, 0x01); # NDL,VLE, REV   
  WriteCD(0x6A, 0x00, 0x00); # set scrolling line  
  #-------------- Partial Display Control ---------#  
  WriteCD(0x80, 0x00, 0x00);  
  WriteCD(0x81, 0x00, 0x00);  
  WriteCD(0x82, 0x00, 0x00);  
  WriteCD(0x83, 0x00, 0x00);  
  WriteCD(0x84, 0x00, 0x00);  
  WriteCD(0x85, 0x00, 0x00);  
  #-------------- Panel Control -------------------#  
  WriteCD(0x90, 0x00, 0x10);  
  WriteCD(0x92, 0x00, 0x00);  
  WriteCD(0x07, 0x01, 0x33); # 262K color and display ON        

def Reset (): # Reset Display
  GPIO.output (RST, True )
  GPIO.output (RST, False )
  time.sleep ( 0.1 )
  GPIO.output (RST, True )
  time.sleep ( 0.1 )
  GPIO.output (CS, True )
  GPIO.output (WR, True )
  time.sleep ( 0.1 )

def WriteCmd (cmd): # Write Command
  for x in range (0,2):
    if (x==0):ccmd=0x00
    else: ccmd=cmd
    GPIO.output (RS, False )  # Register Select = 0
    GPIO.output (CS, False )  # Chip Select = 0
    GPIO.output (D0, False )  
    GPIO.output (D1, False )  
    GPIO.output (D2, False )  
    GPIO.output (D3, False )  
    GPIO.output (D4, False )  
    GPIO.output (D5, False )  
    GPIO.output (D6, False )  
    GPIO.output (D7, False )  
    if (ccmd & 0x01): GPIO.output (D0, True)
    if (ccmd & 0x02): GPIO.output (D1, True)
    if (ccmd & 0x04): GPIO.output (D2, True)
    if (ccmd & 0x08): GPIO.output (D3, True)
    if (ccmd & 0x10): GPIO.output (D4, True)
    if (ccmd & 0x20): GPIO.output (D5, True)
    if (ccmd & 0x40): GPIO.output (D6, True)
    if (ccmd & 0x80): GPIO.output (D7, True)
    GPIO.output (WR, False )  
#    time.sleep ( tdelay )
    GPIO.output (WR, True )  # write the data

def WriteData (cmd): # Write data
    data=cmd
    GPIO.output (RS, True )  # Register Select = 1
    GPIO.output (CS, False )  # Chip Select = 0
    GPIO.output (D0, False )  
    GPIO.output (D1, False )  
    GPIO.output (D2, False )  
    GPIO.output (D3, False )  
    GPIO.output (D4, False )  
    GPIO.output (D5, False )  
    GPIO.output (D6, False )  
    GPIO.output (D7, False )  
    if (data & 0x01): GPIO.output (D0, True)
    if (data & 0x02): GPIO.output (D1, True)
    if (data & 0x04): GPIO.output (D2, True)
    if (data & 0x08): GPIO.output (D3, True)
    if (data & 0x10): GPIO.output (D4, True)
    if (data & 0x20): GPIO.output (D5, True)
    if (data & 0x40): GPIO.output (D6, True)
    if (data & 0x80): GPIO.output (D7, True)
    GPIO.output (WR, False )  
#    time.sleep ( tdelay )
    GPIO.output (WR, True )  # write the data
    
def WriteCD (cmd,data1, data2): #Write command followed by data
    WriteCmd (cmd )
    WriteData (data1)
    WriteData (data2)

def WriteMdata (mdata): #Write multiple data
  for index in range (len(mdata)):
    WriteData (mdata [index])

def Fill (red, green, blue, lines):
  if (red==1):red=255
  if (green==1):green=255
  if (blue==1):blue=255
#  WriteCmd ( 0X22 ) # Next: red, Green, Blue bytes
  pixline = []
  for n in range (240): # Fill screen with color
    pixline.append (blue) # Blue       
    pixline.append (green) # Green       
    pixline.append (red) # Red  
  for n in range (lines):   # 80=one quarter of LCD
    WriteMdata (pixline)

def goto (x, y):  # go to top/bottom
  WriteCD(0x20, 0x00, x); # GRAM horizontal Address
  if (y > 255):WriteCD(0x21, 0x01, y); # GRAM Vertical Adx  
  else: WriteCD(0x21, 0x00, y); # GRAM Vertical Address  
  WriteCmd ( 0X22 ) # Next: red, Green, Blue bytes

def Image (filename):
#  WriteCmd ( 0X22 ) # Next: red, Green, Blue bytes
  try:  # Prevents crashing when images do not work
    with open(filename, 'rb') as bitmap: # 240x320 image
      for x in range ( 0,320 ):
        pixline = []
        for y in range ( 0,720 ): # 720=3x240
#          bitmap.seek(0x36 + x*720 + (719-y)) # 36=header
          bitmap.seek(0x36 + (320-x)*720 + (y)) # flipped 
          Pixel = ord(bitmap.read(1))
          pixline.append (Pixel)
        WriteMdata (pixline)
  except:
      pass

def text(string, red, green, blue):
#  WriteCmd ( 0X22 ) # Next: red, Green, Blue bytes
  string=string.ljust(40, " ") # 240/6=40 characters
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
    WriteMdata (pixline)
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
    WriteMdata (pixline)
    pixline = []

def readport(port):
  GPIO.output(8, GPIO.HIGH) # deselect chip
  GPIO.output(11, GPIO.LOW) # set clock low
  adcin=0
  for shift in range (0,24): # 24 pits shifted
    GPIO.output(8, GPIO.LOW) # select chip
    GPIO.output(10, GPIO.LOW) # low for most bits
    if (shift==7 or shift==8): 
      GPIO.output(10, GPIO.HIGH)
    if (shift==9)and(port & 0x04): 
      GPIO.output(10, GPIO.HIGH)
    if (shift==10)and(port & 0x02): 
      GPIO.output(10, GPIO.HIGH)
    if (shift==11)and(port & 0x01): 
      GPIO.output(10, GPIO.HIGH)
    if (shift > 13)and(GPIO.input(9)):
      adcin = adcin+1 # set bit
    adcin = adcin << 1  # left shift 1
    GPIO.output(11, GPIO.LOW) # cycle the clock
    GPIO.output(11, GPIO.HIGH) 
#  print adcin
  return (adcin)

def sketch():
  for y in range(0,10000):
    pixline=[]
    analogx=(readport(0)/4)
    analogy=(readport(1)/4)
    analogr=(readport(5)/4)
    analogg=(readport(6)/4)
    analogb=(readport(7)/4)
    if analogx>239:analogx=239
    if analogy>239:analogy=239
    goto (analogx, analogy)
    WriteCmd (0X22) # Next: RGB bytes
    pixline.append (analogr)
    pixline.append (analogg)
    pixline.append (analogb)
#    print (analogr)
    WriteMdata (pixline)
    time.sleep(.01)

def scope():
  for x in range(0,320):
    pixline=[]
    alist=(readport(3)/4)
    goto (alist,x)#turned sideways
    WriteCmd (0X22) # Next: RGB bytes
    pixline.append (0xff)
    pixline.append (0xff)
    pixline.append (0xff)
    WriteMdata (pixline)
    
if __name__ == "__main__" :
  init ()
  goto (0, 64)
  Fill (1,0,0,64) # Blue
  goto (0, 128)
  Fill (0,1,0,64) # Green
  goto (0, 192)
  Fill (0,0,1,64) # Red
  goto (0, 256)
  Fill (1,1,1,64) # white
  time.sleep(2)
  
  goto(0,0)
  Image ("Parrots-240.bmp")
  time.sleep(2)

  goto(0,0)
  Fill (0,0,0,320) # black
  scope()
  time.sleep(2)

  goto(0,0)
  Fill (0,0,0,320) # black
  sketch()  #Convert time and date to strings
  time.sleep(2)

  goto(0,0)
  Fill (0,0,0,320) # black
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
  print 'Done'
