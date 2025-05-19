"""
   DWF Python Example
   Author:  Digilent, Inc.
   Revision:  2022-03-08

   Requires:                       
       Python 2.7, 3
"""

from ctypes import *

import math
import time
import sys
from os import sep                # OS specific file path separators
import matplotlib.pyplot as plt
import numpy


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
import dwfconstants as constants

hdwf = c_int()
sts = c_byte()

version = create_string_buffer(16)
dwf.FDwfGetVersion(version)
print("DWF Version: "+str(version.value))

print("Opening first device")
dwf.FDwfDeviceOpen(c_int(-1), byref(hdwf))
# 2nd configuration for Analog Discovery with 16k analog-in buffer
#dwf.FDwfDeviceConfigOpen(c_int(-1), c_int(1), byref(hdwf)) 

if hdwf.value == constants.hdwfNone:
    szError = create_string_buffer(512)
    dwf.FDwfGetLastErrorMsg(szError)
    print("failed to open device\n"+str(szError.value))
    quit()

dwf.FDwfDeviceAutoConfigureSet(hdwf, c_int(0)) # 0 = the device will only be configured when FDwf###Configure is called

print("Generating signal...")
awg_channel = c_int(0)

# enable channel
# The following setup of FDwfAnalogOutNodeEnableSet is for normal use case of generating signal (i.e without modulation) 
#                                    idxChannel AnalogOutNode   fMode
dwf.FDwfAnalogOutNodeEnableSet(hdwf, awg_channel, c_int(0), c_int(1)) 
# idxchannel 0/1 = AWG channel 1/2
# AnalogOutNode (see Figure related to `AnalogOutNode` in `WaveForms SDK Reference Manual.pdf`),
#   in this case, to use normal funciton, it must be set to 0 (i.e Carrier signal)
# fMode 0 (disable carrier), 1 (enable carrier),
#   in this case, because our signal from the carrier, therefore, 
#   fMode = 1 to enable the signal from the carrier node to the output of the enabled channle.

# set function 
#                                       idxChannel    AnalogOutNode func     
dwf.FDwfAnalogOutNodeFunctionSet(hdwf, awg_channel, c_int(0), constants.funcSine)

# set frequency
#                                       idxChannel    AnalogOutNode frequency(Hz)
dwf.FDwfAnalogOutNodeFrequencySet(hdwf, awg_channel, c_int(0), c_double(1e3))

# set offset
dwf.FDwfAnalogOutNodeOffsetSet(hdwf, awg_channel, c_int(0), c_double(0.0))

# set amplitude or DC voltage
dwf.FDwfAnalogOutNodeAmplitudeSet(hdwf, awg_channel, c_int(0), c_double(1.0))

# set running time limit
run_time = 1e-3 # [s]
dwf.FDwfAnalogOutRunSet(hdwf, awg_channel, c_double(run_time))

# set wait time before start
wait = 0 # [s]
dwf.FDwfAnalogOutWaitSet(hdwf, awg_channel, c_double(wait))

# set number of repeating cycles (Armed - Trigger - Wait - Run)
repeat = 1
dwf.FDwfAnalogOutRepeatSet(hdwf, awg_channel, c_int(repeat))

# Set trigger for the ouput AWG
dwf.FDwfAnalogOutTriggerSourceSet(hdwf, awg_channel, constants.trigsrcPC)

# start
# FDwfAnalogOutConfigure(HDWF hdwf, int idxChannel, int fStart)
# fStart – Start the instrument: 0 stop, 1 start, 3 apply
dwf.FDwfAnalogOutConfigure(hdwf, awg_channel, c_int(1))

print("Confiure Oscilloscope...")
osc_ch = c_int(0)

cSamples = 16384
hzRate = 1e6
rgdSamples = (c_double*cSamples)()
cAvailable = c_int()
cLost = c_int()
cCorrupted = c_int()
fLost = 0
fCorrupted = 0

#set up acquisition/ Open oscilloscope
dwf.FDwfAnalogInFrequencySet(hdwf, c_double(hzRate))

# enable all channels
if dwf.FDwfAnalogInChannelEnableSet(hdwf, osc_ch, c_bool(True)) == 0:
    print(f"ERROR")
    
# set offset voltage (in Volts)
offset = 0 # [v]
if dwf.FDwfAnalogInChannelOffsetSet(hdwf, osc_ch, c_double(offset)) == 0:
    print(f"ERROR")
    
# set range (maximum signal amplitude in Volts)
amplitude_range = 5 # [V]
if dwf.FDwfAnalogInChannelRangeSet(hdwf, osc_ch, c_double(amplitude_range)) == 0:
    print(f"ERROR")
    
# set the buffer size (data point in a recording)
if dwf.FDwfAnalogInBufferSizeSet(hdwf, c_int(cSamples)) == 0:
    print(f"ERROR")
    
# set the acquisition frequency (in Hz)
if dwf.FDwfAnalogInFrequencySet(hdwf, c_double(hzRate)) == 0:
    print(f"ERROR")
    
# disable averaging (for more info check the documentation)
if dwf.FDwfAnalogInChannelFilterSet(hdwf, osc_ch, constants.filterDecimate) == 0:
    print(f"ERROR")

#set up trigger
# enable/disable auto triggering
timeout = 0 # disable auto trigger, and set the trigger to **Normal**
if dwf.FDwfAnalogInTriggerAutoTimeoutSet(hdwf, c_double(timeout)) == 0:
    print(f"ERROR")

# set trigger source
if dwf.FDwfAnalogInTriggerSourceSet(hdwf, constants.trigsrcAnalogOut1) == 0: # AWG 1
    print(f"ERROR")

# set trigger channel
if dwf.FDwfAnalogInTriggerChannelSet(hdwf, osc_ch) == 0:
    print(f"ERROR")

# set trigger type
if dwf.FDwfAnalogInTriggerTypeSet(hdwf, constants.trigtypeEdge) == 0:
    print(f"ERROR")

# set trigger level
level = 0 # [V]
if dwf.FDwfAnalogInTriggerLevelSet(hdwf, c_double(level)) == 0:
    print(f"ERROR")

# set trigger edge
if dwf.FDwfAnalogInTriggerConditionSet(hdwf, constants.trigcondRisingPositive) == 0:
    print(f"ERROR")


#FDwfAnalogInConfigure(HDWF hdwf, int fReconfigure, int fStart)
if dwf.FDwfAnalogInConfigure(hdwf, c_bool(False), c_bool(True)) == 0:
        print(f"ERROR")
# wait at least 2 seconds with Analog Discovery for the offset to stabilize, before the first reading after device open or offset/range change
time.sleep(2)

print("Starting repeated acquisitions")
# Trigger the AWG
dwf.FDwfDeviceTriggerPC(hdwf)

    
    # read data to an internal buffer
while True:
        status = c_byte()    # variable to store buffer status
        if dwf.FDwfAnalogInStatus(hdwf, c_bool(True), byref(status)) == 0:
            print(f"ERROR")
    
        # check internal buffer status
        if status.value == constants.DwfStateDone.value:
                # exit loop when ready
                break
    
    # copy buffer
if dwf.FDwfAnalogInStatusData(hdwf, osc_ch, rgdSamples, c_int(cSamples)) == 0:
    print(f"ERROR")
    
# convert into list
rgdSamples = [float(element) for element in rgdSamples]
# print(rgdSamples)

# FDwfAnalogOutReset(HDWF hdwf, int idxChannel)
dwf.FDwfAnalogOutReset(hdwf, awg_channel)

# FDwfAnalogOutConfigure(HDWF hdwf, int idxChannel, int fStart)
# fStart – Start the instrument: 0 stop, 1 start, 3 apply.
dwf.FDwfAnalogOutConfigure(hdwf, c_int(0), c_int(0))
dwf.FDwfDeviceCloseAll()


# generate buffer for time moments
time = []
for index in range(len(rgdSamples)):
            time.append(index * 1e03 / hzRate)   # convert time to ms

# plot
plt.plot(time, rgdSamples)
plt.xlabel("time [ms]")
plt.ylabel("voltage [V]")
plt.show()

