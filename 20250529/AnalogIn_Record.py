"""
   DWF Python Example
   Author:  Digilent, Inc.
   Modified: Tran Le Phuong Lan
   Revision:  2025-05-29

   Reference: https://forum.digilent.com/topic/23122-lost-and-corrupted-data-analog-discovery-pro/

   Requires:                       
       Python 2.7, 3
"""
from ctypes import *
import sys
import os
from os import sep  

if sys.platform.startswith("win"):
    dwf = cdll.dwf
    constants_path = "C:" + sep + "Program Files (x86)" + sep + "Digilent" + sep + "WaveFormsSDK" + sep + "samples" + sep + "py"
elif sys.platform.startswith("darwin"): # on macOS
    dwf = cdll.LoadLibrary("/Library/Frameworks/dwf.framework/dwf")
else: # on Linux
    dwf = cdll.LoadLibrary("libdwf.so")
    constants_path = sep + "usr" + sep + "share" + sep + "digilent" + sep + "waveforms" + sep + "samples" + sep + "py"

# Import constans
sys.path.append(constants_path)
import dwfconstants


from dwfconstants import *
import math
import time
import matplotlib.pyplot as plt
# import sys
import numpy as np

if sys.platform.startswith("win"):
    dwf = cdll.dwf
elif sys.platform.startswith("darwin"):
    dwf = cdll.LoadLibrary("/Library/Frameworks/dwf.framework/dwf")
else:
    dwf = cdll.LoadLibrary("libdwf.so")

#declare ctype variables
hdwf = c_int()
sts = c_byte()
hzAcq = c_double(200)
# This is the PC buffer (or recorded file in the computer).
# It is TOTALLY DIFFERENT FROM the internal buffer (of the FPGA, which is around 32K samples) 
# of the analog-in channels of the Analog Device 3.
# The PC buffer limit only decided by the available disk space in PC, which this code is run.
nSamples = 500# 200000
rgdSamples = (c_double*nSamples)()
cAvailable = c_int()
cLost = c_int()
cCorrupted = c_int()
fLost = 0
fCorrupted = 0

#print(DWF version
version = create_string_buffer(16)
dwf.FDwfGetVersion(version)
print("DWF Version: "+str(version.value))

#open device
print("Opening first device")
dwf.FDwfDeviceOpen(c_int(-1), byref(hdwf))

if hdwf.value == hdwfNone.value:
    szerr = create_string_buffer(512)
    dwf.FDwfGetLastErrorMsg(szerr)
    print(str(szerr.value))
    print("failed to open device")
    quit()

dwf.FDwfDeviceAutoConfigureSet(hdwf, c_int(0)) # 0 = the device will only be configured when FDwf###Configure is called

print("Generating sine wave...")
dwf.FDwfAnalogOutNodeEnableSet(hdwf, c_int(0), AnalogOutNodeCarrier, c_int(1))
dwf.FDwfAnalogOutNodeFunctionSet(hdwf, c_int(0), AnalogOutNodeCarrier, funcSine)
dwf.FDwfAnalogOutNodeFrequencySet(hdwf, c_int(0), AnalogOutNodeCarrier, c_double(1))
dwf.FDwfAnalogOutNodeAmplitudeSet(hdwf, c_int(0), AnalogOutNodeCarrier, c_double(2))
dwf.FDwfAnalogOutConfigure(hdwf, c_int(0), c_int(1))

#set up acquisition
dwf.FDwfAnalogInChannelEnableSet(hdwf, c_int(0), c_int(1))
dwf.FDwfAnalogInChannelRangeSet(hdwf, c_int(0), c_double(5))
dwf.FDwfAnalogInAcquisitionModeSet(hdwf, acqmodeRecord)
dwf.FDwfAnalogInFrequencySet(hdwf, hzAcq)
dwf.FDwfAnalogInRecordLengthSet(hdwf, c_double(-1)) # c_double(nSamples/hzAcq.value), -1 infinite record length 
dwf.FDwfAnalogInConfigure(hdwf, c_int(1), c_int(0))

#wait at least 2 seconds for the offset to stabilize
time.sleep(2)

print("Starting oscilloscope")
dwf.FDwfAnalogInConfigure(hdwf, c_int(0), c_int(1))

plt.axis([0, nSamples / hzAcq.value, -5, 5])
plt.ion()
hl, = plt.plot([], [])


cSamples = 0
print("Press Ctrl+C to stop")
while cSamples < nSamples:
    dwf.FDwfAnalogInStatus(hdwf, c_int(1), byref(sts))
    if cSamples == 0 and (sts == DwfStateConfig or sts == DwfStatePrefill or sts == DwfStateArmed) :
        # Acquisition not yet started.
        continue

    dwf.FDwfAnalogInStatusRecord(hdwf, byref(cAvailable), byref(cLost), byref(cCorrupted))
    
    cSamples += cLost.value

    if cLost.value :
        fLost = 1
    if cCorrupted.value :
        fCorrupted = 1

    # Either **print debug message** or **plot the animated plot hl** below
    ## **print debug message**
    if cAvailable.value==0 :
        dwf.FDwfAnalogInStatus(hdwf, c_int(1), byref(sts))
        print(f"wehn {cAvailable.value=}, the {sts}")
        continue
    else:
        dwf.FDwfAnalogInStatus(hdwf, c_int(1), byref(sts))
        print(f"when {cAvailable.value=}, the {sts}")

    if cSamples+cAvailable.value > nSamples :
        cAvailable = c_int(nSamples-cSamples)
    
    dwf.FDwfAnalogInStatusData(hdwf, c_int(0), byref(rgdSamples, sizeof(c_double)*cSamples), cAvailable) # get channel 1 data
    #dwf.FDwfAnalogInStatusData(hdwf, c_int(1), byref(rgdSamples, sizeof(c_double)*cSamples), cAvailable) # get channel 2 data
    cSamples += cAvailable.value

    ## **plot the animated plot hl**
    # hl.set_xdata(np.arange(0, cSamples, 1) / hzAcq.value)
    # list_rg = list(rgdSamples)
    # hl.set_ydata(list_rg[0:cSamples])
    # plt.draw()
    # plt.pause(0.01)

dwf.FDwfAnalogOutReset(hdwf, c_int(0))
dwf.FDwfDeviceCloseAll()

print("Recording done")
print(f"{fLost=}")
print(f"{fCorrupted=}")
# if fLost:
#     print("Samples were lost! Reduce frequency")
# if fCorrupted:
#     print("Samples could be corrupted! Reduce frequency")

# f = open("record.csv", "w")
# for v in rgdSamples:
#     f.write("%s\n" % v)
# f.close()


