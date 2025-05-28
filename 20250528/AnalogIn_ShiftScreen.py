"""
   DWF Python Example
   Author:  Digilent, Inc.
   Revision:  2018-07-19

   Requires:                       
       Python 2.7, 3
"""

from ctypes import *
import math
import time
import matplotlib.pyplot as plt
import sys

if sys.platform.startswith("win"):
    dwf = cdll.dwf
elif sys.platform.startswith("darwin"):
    dwf = cdll.LoadLibrary("/Library/Frameworks/dwf.framework/dwf")
else:
    dwf = cdll.LoadLibrary("libdwf.so")

hdwf = c_int()
sts = c_byte()
hzAcq = c_double(500)
nSamples = 1000
rgdSamples = (c_double*nSamples)()
cValid = c_int(0)

version = create_string_buffer(16)
dwf.FDwfGetVersion(version)
print("DWF Version: "+str(version.value))

print("Opening first device")
dwf.FDwfDeviceOpen(c_int(-1), byref(hdwf))

if hdwf.value == 0:
    szerr = create_string_buffer(512)
    dwf.FDwfGetLastErrorMsg(szerr)
    print(str(szerr.value))
    print("failed to open device")
    quit()

dwf.FDwfDeviceAutoConfigureSet(hdwf, c_int(0)) # 0 = the device will only be configured when FDwf###Configure is called

print("Generating sine wave...")
dwf.FDwfAnalogOutNodeEnableSet(hdwf, c_int(0), c_int(0), c_int(1))
dwf.FDwfAnalogOutNodeFunctionSet(hdwf, c_int(0), c_int(0), c_int(1)) #sine
dwf.FDwfAnalogOutOffsetSet(hdwf, c_int(0), c_double(1))
dwf.FDwfAnalogOutNodeFrequencySet(hdwf, c_int(0), c_int(0), c_double(1))
dwf.FDwfAnalogOutNodeAmplitudeSet(hdwf, c_int(0), c_int(0), c_double(3))
dwf.FDwfAnalogOutConfigure(hdwf, c_int(0), c_int(1))

#set up acquisition
dwf.FDwfAnalogInChannelEnableSet(hdwf, c_int(0), c_int(1))
success = dwf.FDwfAnalogInChannelRangeSet(hdwf, c_int(0), c_double(20))
if success:
    print(f"set range OK")
else:
    print(f"set range ERROR")
dwf.FDwfAnalogInAcquisitionModeSet(hdwf, c_int(1)) #acqmodeScanShift
dwf.FDwfAnalogInFrequencySet(hdwf, hzAcq)
dwf.FDwfAnalogInBufferSizeSet(hdwf, c_int(nSamples))
dwf.FDwfAnalogInConfigure(hdwf, c_int(1), c_int(0))

# print out default settings
# FDwfAnalogInChannelRangeGet(HDWF hdwf, int idxChannel, double *pvoltsRange)
pvoltsRange= c_double(0)
dwf.FDwfAnalogInChannelRangeGet(hdwf, c_int(0), byref(pvoltsRange))
print(f"set range: {pvoltsRange=}")

# FDwfAnalogInChannelRangeInfo(HDWF hdwf, double *pvoltsMin, double *pvoltsMax, double *pnSteps);
pvoltsMin= c_double()
pvoltsMax= c_double()
pnSteps= c_double()
dwf.FDwfAnalogInChannelRangeInfo(hdwf, byref(pvoltsMin), byref(pvoltsMax), byref(pnSteps))
print(f"{pvoltsMin=}")
print(f"{pvoltsMax=}")
print(f"{pnSteps=}")

# FDwfAnalogInChannelAttenuationGet(HDWF hdwf, int idxChannel, double *pxAttenuation);
pxAttenuation = c_double()
dwf.FDwfAnalogInChannelAttenuationGet(hdwf, c_int(0), byref(pxAttenuation));
print(f"{pxAttenuation=}")

#wait at least 2 seconds for the offset to stabilize
time.sleep(2)

#begin acquisition
dwf.FDwfAnalogInConfigure(hdwf, c_int(0), c_int(1))

plt.axis([0, len(rgdSamples), -5, 5])
plt.ion()
hl, = plt.plot([], [])
hl.set_xdata(range(0, len(rgdSamples)))

start = time.time()
print("Press Ctrl+C to stop")
try:
    while True: #time.time()-start < 10:
        dwf.FDwfAnalogInStatus(hdwf, c_int(1), byref(sts))

        dwf.FDwfAnalogInStatusSamplesValid(hdwf, byref(cValid))

        dwf.FDwfAnalogInStatusData(hdwf, c_int(0), byref(rgdSamples), cValid) # get channel 1 data
        #dwf.FDwfAnalogInStatusData(hdwf, c_int(1), byref(rgdSamples), cValid) # get channel 2 data
        #print(cValid.value)
        print(f"{sts=}")
        print(f"{cValid.value=}")
        print(f"{rgdSamples[0:10]=}")
        hl.set_ydata(rgdSamples)
        plt.draw()
        plt.pause(0.1)
except KeyboardInterrupt:
    pass

dwf.FDwfAnalogOutConfigure(hdwf, c_int(0), c_int(0))
dwf.FDwfDeviceCloseAll()

