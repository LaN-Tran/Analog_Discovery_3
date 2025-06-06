"""
   DWF Python Example
   Author:  Digilent, Inc.
   Revision:  2025-04-14

   Requires:                       
       Python 2.7, 3
"""

from ctypes import *
from dwfconstants import *
import time
import sys

if sys.platform.startswith("win"):
    dwf = cdll.dwf
elif sys.platform.startswith("darwin"):
    dwf = cdll.LoadLibrary("/Library/Frameworks/dwf.framework/dwf")
else:
    dwf = cdll.LoadLibrary("libdwf.so")

hdwf = c_int()
sts = c_byte()
IsEnabled = c_int()
vpp = c_double()
vpn = c_double()
app = c_double()
apn = c_double()

version = create_string_buffer(16)
dwf.FDwfGetVersion(version)
print("DWF Version: "+str(version.value))

print("Opening first device")
dwf.FDwfDeviceOpen(-1, byref(hdwf))

if hdwf.value == hdwfNone.value:
    print("failed to open device")
    quit()

dwf.FDwfDeviceAutoConfigureSet(hdwf, 0)

# enable positive supply
dwf.FDwfAnalogIOChannelNodeSet(hdwf, 0, 0, c_double(1)) 
# set voltage to 5 V
dwf.FDwfAnalogIOChannelNodeSet(hdwf, 0, 1, c_double(15.0)) 
# set current limit to 500mA
dwf.FDwfAnalogIOChannelNodeSet(hdwf, 0, 2, c_double(0.5)) 
# enable negative supply
dwf.FDwfAnalogIOChannelNodeSet(hdwf, 1, 0, c_double(1)) 
# set voltage to -5 V
dwf.FDwfAnalogIOChannelNodeSet(hdwf, 1, 1, c_double(-15.0)) 
# set current limit to -500mA
dwf.FDwfAnalogIOChannelNodeSet(hdwf, 1, 2, c_double(-0.5)) 
# master enable
dwf.FDwfAnalogIOEnableSet(hdwf, 1)
# configure device analog-io
dwf.FDwfAnalogIOConfigure(hdwf)

for i in range(1, 11):
    # wait 1 second between readings
    time.sleep(1.0)
    # fetch analogIO status from device
    if dwf.FDwfAnalogIOStatus(hdwf) == 0:
        break

    # voltage readback
    dwf.FDwfAnalogIOChannelNodeStatus(hdwf, 0, 1, byref(vpp))
    dwf.FDwfAnalogIOChannelNodeStatus(hdwf, 0, 2, byref(app))
    dwf.FDwfAnalogIOChannelNodeStatus(hdwf, 1, 1, byref(vpn))
    dwf.FDwfAnalogIOChannelNodeStatus(hdwf, 1, 2, byref(apn))
    
    print("Positive Supply: " + str(round(vpp.value,3)) + " V  " + str(round(app.value,3)) + " A")
    print("Negative Supply: " + str(round(vpn.value,3)) + " V  " + str(round(apn.value,3)) + " A")

dwf.FDwfDeviceClose(hdwf)
