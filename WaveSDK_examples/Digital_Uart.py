"""
   DWF Python Example
   Author:  Digilent, Inc.
   Revision:  2018-07-23

   Requires:                       
       Python 2.7, 3
"""

from ctypes import *
import math
import sys
import time

if sys.platform.startswith("win"):
    dwf = cdll.LoadLibrary("dwf.dll")
elif sys.platform.startswith("darwin"):
    dwf = cdll.LoadLibrary("/Library/Frameworks/dwf.framework/dwf")
else:
    dwf = cdll.LoadLibrary("libdwf.so")

hdwf = c_int()

print("Opening first device")
dwf.FDwfDeviceOpen(-1, byref(hdwf))
# device configuration of index 3 (4th) for Analog Discovery has 16kS digital-in/out buffer
#dwf.FDwfDeviceConfigOpen(c_int(-1), c_int(3), byref(hdwf)) 

if hdwf.value == 0:
    print("failed to open device")
    szerr = create_string_buffer(512)
    dwf.FDwfGetLastErrorMsg(szerr)
    print(str(szerr.value))
    quit()

print("Configuring UART...")

cRX = c_int(0)
fParity = c_int(0)

# configure the I2C/TWI, default settings
dwf.FDwfDigitalUartRateSet(hdwf, c_double(9600)) # 9.6kHz
dwf.FDwfDigitalUartTxSet(hdwf, 0) # TX = DIO-0
dwf.FDwfDigitalUartRxSet(hdwf, 1) # RX = DIO-1
dwf.FDwfDigitalUartBitsSet(hdwf, 8) # 8 bits
dwf.FDwfDigitalUartParitySet(hdwf, 0) # 0 no parity, 1 even, 2 odd, 3 mark (high), 4 space (low)
dwf.FDwfDigitalUartStopSet(hdwf, c_double(1)) # 1 bit stop length

dwf.FDwfDigitalUartTx(hdwf, None, 0)# initialize TX, drive with idle level
dwf.FDwfDigitalUartRx(hdwf, None, 0, byref(cRX), byref(fParity))# initialize RX reception
time.sleep(1)

rgTX = create_string_buffer(b'Hello\r\n')
rgRX = create_string_buffer(8193)

print("Sending on TX for 10 seconds...")
dwf.FDwfDigitalUartTx(hdwf, rgTX, sizeof(rgTX)-1) # send text, trim zero ending

tsec = time.perf_counter()  + 10 # receive for 10 seconds
print("Receiving on RX...")
while time.perf_counter() < tsec:
    time.sleep(0.01)
    dwf.FDwfDigitalUartRx(hdwf, rgRX, sizeof(rgRX)-1, byref(cRX), byref(fParity)) # read up to 8k chars at once
    if cRX.value > 0:
        rgRX[cRX.value] = 0 # add zero ending
        print(rgRX.value.decode(), end = '', flush=True)
    if fParity.value != 0:
        print("Parity error {}".format(fParity.value))

dwf.FDwfDeviceCloseAll()
