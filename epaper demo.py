# ------------------------------------------------------
# Demo program for the Raspberry Pi Pico W with the WeAct Studio 1.54" Epaper Module
#
#     Wiring Configuration
#   +-----------+-----------+
#   | Display   | Pi Pico W |
#   | 1 Busy ---|----- GP14 |
#   | 2 RES ----|----- GP15 |
#   | 3 D/C ----|----- GP12 |
#   | 4 CS -----|----- GP13 |
#   | 5 SCL ----|----- GP11 |
#   | 6 SDA ----|----- GP10 |
#   | 7 GND ----|------ GND |
#   | 8 VCC ----|----- 3.3V |
#   +-----------+-----------+
#
# ------------------------------------------------------

from machine import Pin, SPI
import time
from epaper import EPaper

# ------------------------------------------------------
# Initialize SPI
spi = SPI(1, baudrate=2000000, polarity=0, phase=0, sck=Pin(10), mosi=Pin(11))

# ------------------------------------------------------
# Create ePaper instance
epaper = EPaper(spi, cs=13, dc=12, rst=15, busy=14)

# ------------------------------------------------------
# Clear Display

epaper.clear(1) #(c)

  # c  Colour of the clear (0 Black / 1 White)

# ------------------------------------------------------
# Draw  a filled Vertical Line

epaper.vline(5,110,85,0) #Vertical Line (x,y,h,c)

  # x  Starting X Coordinate
  # y  Starting Y Coordinate
  # w  Line Length (Height)
  # c  Colour of the line (0 Black / 1 White)
  
# ------------------------------------------------------
# Draw Horizontal Line

epaper.hline(5,5,190,0) #(x,y,w,c)

  # x  Starting X Coordinate
  # y  Starting Y Coordinate
  # w  Line Length (Width)
  # c  Colour of the line (0 Black / 1 White)
  
# ------------------------------------------------------
# Write Text

epaper.text("PicoW-WeActStudio Epaper", 5, 10, 0) #(t,x,y,c)

  # t  Text
  # x  Starting X Coordinate
  # y  Starting Y Coordinate
  # c  Colour of the text (0 Black / 1 White)

# ------------------------------------------------------
# Draw Line

epaper.line(5,20,195,20,0) #(x1,y1,x2,y2)

  # x1  Starting X Coordinate
  # y1  Starting Y Coordinate
  # x2  Ending X Coordinate
  # y2  Ending Y Coordinate
  # c  Colour of the line (0 Black / 1 White)

# ------------------------------------------------------
# Draw a Rectangle

epaper.rect(5,25,190,50,0) #Rectangle (x,y,w,h,c)

  # x  Starting X Coordinate
  # y  Starting Y Coordinate
  # w  Width of Rectangle (Direction is right)
  # h  Height of Rectangle (Direction is down)
  # c  Colour of the outline line (0 Black / 1 White)

# ------------------------------------------------------
# Draw a filled Rectangle

epaper.fill_rect(5,80,190,25,0) #Filled Rectangle (x,y,w,h,c)

  # x  Starting X Coordinate
  # y  Starting Y Coordinate
  # w  Width of Rectangle (Direction is right)
  # h  Height of Rectangle (Direction is down)
  # c  Colour of the filled rectangle (0 Black / 1 White)

# ------------------------------------------------------
# Draw a Circle

epaper.circle(30,50,15,0,0) #(x,y,r,c,f)

  # x  Centre X Coordinate
  # y  Centre Y Coordinate
  # r  Raduius of Circle
  # c  Colour of the Circle (0 Black / 1 White)
  # f  Filled (0 Outline Only / 1 Filled)

epaper.circle(60,40,10,0,1)

# ------------------------------------------------------
# Draw an Ellipse

epaper.ellipse(95,60,30,10,0,0) #(x,y,xr,yr,c,f)

  # x  Centre X Coordinate
  # y  Centre Y Coordinate
  # xr X Raduius of Ellipse
  # yr Y Raduius of Ellipse
  # c  Colour of the Circle (0 Black / 1 White)
  # f  Filled (0 Outline Only / 1 Filled)
  
epaper.ellipse(145,40,40,10,0,1) #(x,y,xr,yr,c,f)

# ------------------------------------------------------
# Draw a Circle Quadrant

epaper.qtrcircle(30,130,15,0,0,"1010") #(x,y,r,c,f,q)

  # x  Centre X Coordinate
  # y  Centre Y Coordinate
  # r  Raduius of Circle
  # c  Colour of the Circle (0 Black / 1 White)
  # f  Filled (0 Outline Only / 1 Filled)
  # q  Quadrant ("1234")
         # 1  Bottom Right Quadrant (0 hide / 1 Draw)
         # 2  Bottom Left Quadrant  (0 hide / 1 Draw)
         # 3  Top Left Quadrant     (0 hide / 1 Draw)
         # 4  Top Right Quadrant    (0 hide / 1 Draw)
         # eg: "1010" prints the Bottom Right and Top Left Quadrants

epaper.qtrcircle(30,130,15,0,1,"0101") #(x,y,r,c,f,q)

# ------------------------------------------------------
# Draw a Rounded Corner Rectangle

epaper.rndrect(55,115,60,60,0,0,15) #(x,y,w,h,c,f,r)

  # x  Starting X Coordinate
  # y  Starting Y Coordinate
  # w  Width of Rectangle (Direction is right)
  # h  Height of Rectangle (Direction is down)
  # c  Colour of the filled rectangle (0 Black / 1 White)
  # f  Filled (0 Outline Only / 1 Filled)
  # r  Radius of Corner

epaper.rndrect(125,115,60,80,0,1,20)

# ------------------------------------------------------
# Write to Display

epaper.show()

  # Forces full refresh of the display and writes the buffered data