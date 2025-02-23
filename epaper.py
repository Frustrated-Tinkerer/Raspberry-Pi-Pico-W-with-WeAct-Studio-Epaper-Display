from machine import Pin, SPI
import framebuf
import time
import math

class EPaper:
    def __init__(self, spi, cs, dc, rst, busy):
        self.spi = spi
        self.cs = Pin(cs, Pin.OUT, value=1)
        self.dc = Pin(dc, Pin.OUT, value=0)
        self.rst = Pin(rst, Pin.OUT, value=1)
        self.busy = Pin(busy, Pin.IN)

        self.width = 200
        self.height = 200
        self.buffer = bytearray(self.width * self.height // 8)
        self.fb = framebuf.FrameBuffer(self.buffer, self.width, self.height, framebuf.MONO_HLSB)

        self.init_display()

    def send_command(self, command):
        self.dc.value(0)
        self.cs.value(0)
        self.spi.write(bytes([command]))
        self.cs.value(1)

    def send_data(self, data):
        self.dc.value(1)
        self.cs.value(0)
        self.spi.write(bytes([data]))
        self.cs.value(1)

    def wait_busy(self):
        while self.busy.value() == 1:
            time.sleep(0.1)

    def reset(self):
        self.rst.value(0)
        time.sleep(0.1)
        self.rst.value(1)
        time.sleep(0.1)

    def init_display(self):
        self.reset()
        self.send_command(0x12)  # Software Reset
        self.wait_busy()
        self.send_command(0x01)  # Driver output control
        self.send_data(0xC7)
        self.send_data(0x00)
        self.send_data(0x01)

    def show(self):
        self.send_command(0x24)
        for byte in self.buffer:
            self.send_data(byte)
        self.send_command(0x22)  # Display update control
        self.send_data(0xF7)
        self.send_command(0x20)  # Activate display update
        self.wait_busy()

    def clear(self, colour):
        self.fb.fill(colour)
        self.show()

    def text(self, text, x, y, c):
        self.fb.text(text, x, y, c)
    
    def line(self, x1, y1, x2, y2, c): #Line
        self.fb.line(x1, y1, x2, y2, c)
        
    def rect(self, x, y, w, h, c): #Rectangle
        self.fb.rect(x, y, w, h, c, 0)
        
    def fill_rect(self, x, y, w, h, c): #Filled Rectangle
        self.fb.fill_rect(x, y, w, h, c)
        
    def hline(self, x, y, w, c): #Horizontal Line
        self.fb.hline(x, y, w, c)
        
    def vline(self, x, y, h, c): #Vertical Line
        self.fb.vline(x, y, h, c)
    
    def ellipse(self,x,y,xr,yr,c,f): #Ellipse
        self.fb.ellipse(x, y, xr, yr, c, f)

    def circle(self, x, y, r, c, f): #Circle
        self.fb.ellipse(x, y, r, r, c, f)
        
    def qtrcircle(self, x, y, r, c, f, q): #Qtr Circle
        mask = int(q,2)
        self.fb.ellipse(x, y, r, r, c, f, mask)
    
    def rndrect(self, x, y, w, h, c, f, r): #Rounded Corner Rectangle
        
        # Top Line (Used no Fill)
        tlx = x + r        # Top Line X Start (Corner Adjusted)
        tly = y            # Top Line Y Start (Corner Adjusted)
        tlw = w - (2 * r)  # Top Line Width (Corner Adjusted)
        
        # Bottom Line (Used no Fill)
        blx = x + r        # Bottom Line X Start (Corner Adjusted)
        bly = y + h        # Bottom Line X Start (Corner Adjusted)
        blw = w - (2 * r)  # Bottom Line Width (Corner Adjusted)
        
        # Left Line (Used no Fill)
        llx = x            # Left Line X Start (Corner Adjusted)
        lly = y + r        # Left Line Y Start (Corner Adjusted)
        llh = h - (2 * r)  # Left Line Height (Corner Adjusted)
        
        # Right Line (Used no Fill)
        rlx = x + w        # Right Line X Start (Corner Adjusted)
        rly = y + r        # Right Line Y Start (Corner Adjusted)
        rlh = h - (2 * r)  # Right Line Height (Corner Adjusted)
        
        # Top Rectangle (Used with Fill)
        xtr = x + r        # Top Rectangle X Start (Corner Adjusted)
        ytr = y            # Top Rectangle Y Start (Corner Adjusted)
        wtr = w - (2 * r)  # Top Rectangle Width (Corner Adjusted)
        htr = r            # Top Rectangle Height (Corner Adjusted)
        xbr = x + r        # Bottom Rectangle X Start (Corner Adjusted)
        ybr = y + h - r    # Bottom Rectangle Y Start (Corner Adjusted)
        wbr = w - (2 * r)  # Bottom Rectangle Width (Corner Adjusted)
        hbr = r + 1        # Bottom Rectangle Height (Corner Adjusted)
        xlr = x            # Left Rectangle X Start (Corner Adjusted)
        ylr = y + r        # Left Rectangle Y Start (Corner Adjusted)
        wlr = r            # Left Rectangle Width (Corner Adjusted)
        hlr = h - (2 * r)  # Left Rectangle Height (Corner Adjusted)
        xrr = x + w - r    # Right Rectangle X Start (Corner Adjusted)
        yrr = y + r        # Right Rectangle Y Start (Corner Adjusted)
        wrr = r + 1        # Right Rectangle Width (Corner Adjusted)
        hrr = h - (2 * r)  # Right Rectangle Height (Corner Adjusted)
        xmr = x + r        # Middle Rectangle X Start (Corner Adjusted)
        ymr = y + r        # Middle Rectangle Y Start (Corner Adjusted)
        wmr = w - (2 * r)  # Middle Rectangle Width (Corner Adjusted)
        hmr = h - (2 * r)  # Middle Rectangle Height (Corner Adjusted)
        
        # Corner Centres (Used with and without Fill)
        tlcx = x + r       # Top Left Corner X
        tlcy = y + r       # Top Left Corner Y
        trcx = x + w - r   # Top Right Corner X
        trcy = y + r       # Top Right Corner Y
        blcx = x + r       # Bottom Left Corner X
        blcy = y + h - r   # Bottom Left Corner Y
        brcx = x + w - r   # Bottom Right Corner X
        brcy = y + h - r   # Bottom Right Corner Y
        
        if (f == 0): # No Fill
            self.fb.hline(tlx, tly, tlw, c) # Top Line
            self.fb.hline(blx, bly, blw, c) # Bottom Line
            self.fb.vline(llx, lly, llh, c) # Left Line
            self.fb.vline(rlx, rly, rlh, c) # Left Line
            self.fb.ellipse(tlcx, tlcy, r, r, c, 0, 0x2) #Top Left Corner
            self.fb.ellipse(trcx, trcy, r, r, c, 0, 0x1) # Top Right Corner
            self.fb.ellipse(blcx, blcy, r, r, c, 0, 0x4) # Bottom Left Corner
            self.fb.ellipse(brcx, brcy, r, r, c, 0, 0x8) # Bottom Right Corner
        
        else: # Filled
            self.fb.fill_rect(xtr, ytr, wtr, htr, c) # Top Rectangle
            self.fb.fill_rect(xbr, ybr, wbr, hbr, c) # Bottom Rectangle
            self.fb.fill_rect(xlr, ylr, wlr, hlr, c) # Left Rectangle
            self.fb.fill_rect(xrr, yrr, wrr, hrr, c) # Right Rectangle
            self.fb.fill_rect(xmr, ymr, wmr, hmr, c) # Right Rectangle
            self.fb.ellipse(tlcx, tlcy, r, r, c, 1, 0x2) #Top Left Corner
            self.fb.ellipse(trcx, trcy, r, r, c, 1, 0x1) # Top Right Corner
            self.fb.ellipse(blcx, blcy, r, r, c, 1, 0x4) # Bottom Left Corner
            self.fb.ellipse(brcx, brcy, r, r, c, 1, 0x8) # Bottom Right Corner            
        
        
        