"""
   DWF Python Example
   Author:  Digilent, Inc.
   Revision:  2023-10-19

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
voltage = c_double()
current = c_double()

version = create_string_buffer(16)
dwf.FDwfGetVersion(version)
print("DWF Version: "+str(version.value))

dwf.FDwfParamSet(DwfParamOnClose, 0) # 0 = run, 1 = stop, 2 = shutdown

print("Opening first device")
dwf.FDwfDeviceOpen(-1, byref(hdwf))

if hdwf.value == hdwfNone.value:
    print("failed to open device")
    quit()

dwf.FDwfDeviceAutoConfigureSet(hdwf, 0) # 0 = the device will only be configured when FDwf###Configure is called

# set digital voltage between 1.2 and 3.3V
dwf.FDwfAnalogIOChannelNodeSet(hdwf, 0, 0, c_double(1.8))
# enable VIO output
dwf.FDwfAnalogIOEnableSet(hdwf, 1)

# configure week pull for DIN lines, 0.0 low, 0.5 middle, 1 high
dwf.FDwfAnalogIOChannelNodeSet(hdwf, 0, 1, c_double(0.5)) 

# pull enable for DIO 39 to 24, bit 15 to 0
dwf.FDwfAnalogIOChannelNodeSet(hdwf, 0, 2, c_double(0x0081)) # DIO7 and DIO0
# pull up/down for DIO
dwf.FDwfAnalogIOChannelNodeSet(hdwf, 0, 3, c_double(0x0080)) # DIO7 pull up and DIO0 pull down

# drive strength for DIO lines: 0 (auto based on digital voltage), 2, 4, 6, 8, 12, 16 (mA)
dwf.FDwfAnalogIOChannelNodeSet(hdwf, 0, 4, c_double(8)) 
# slew rate for DIO lines: 0 quietio, 1 slow, 2 fast
dwf.FDwfAnalogIOChannelNodeSet(hdwf, 0, 5, c_double(1)) 

dwf.FDwfAnalogIOConfigure(hdwf)

for i in range(1, 11):
    #wait 1 second between readings
    time.sleep(1)
    #fetch analogIO status from device
    if dwf.FDwfAnalogIOStatus(hdwf) == 0:
        break

    # USB monitor
    dwf.FDwfAnalogIOChannelNodeStatus(hdwf, 2, 0, byref(voltage))
    dwf.FDwfAnalogIOChannelNodeStatus(hdwf, 2, 1, byref(current))
    print("USB: " + str(round(voltage.value,3)) + "V\t" + str(round(current.value,3)) + "A")
    
    # VIO monitor
    dwf.FDwfAnalogIOChannelNodeStatus(hdwf, 1, 0, byref(voltage))
    dwf.FDwfAnalogIOChannelNodeStatus(hdwf, 1, 1, byref(current))
    print("VIO: " + str(round(voltage.value,3)) + "V\t" + str(round(current.value,3)) + "A")

    # in case of over-current condition the supplies are disabled
    dwf.FDwfAnalogIOEnableStatus(hdwf, byref(IsEnabled))
    if not IsEnabled:
        #re-enable supplies
        print("Restart")
        dwf.FDwfAnalogIOEnableSet(hdwf, c_int(False)) 
        dwf.FDwfAnalogIOConfigure(hdwf)
        dwf.FDwfAnalogIOEnableSet(hdwf, c_int(True))
        dwf.FDwfAnalogIOConfigure(hdwf)

#close the device
dwf.FDwfDeviceClose(hdwf)
