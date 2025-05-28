# Problems

- 1. When `dwf.FDwfAnalogInChannelRangeSet(hdwf, oscilloscope_ch, c_double(4))`, and the generated signal positive/negative max amplitude by the wavegenerator is always cut back to 2.5V / -2.5V. That means the range set of the oscilloscope is wrong. but why wrong? to answer this question, it leads to the **problem 2** below: 

- 2. set range (unit V) with this command for an oscilloscope channel `dwf.FDwfAnalogInChannelRangeSet(hdwf, oscilloscope_ch, c_double(1))`, but result returned by `dwf.FDwfAnalogInChannelRangeInfo(hdwf, byref(pvoltsMin), byref(pvoltsMax), byref(pnSteps))` is `pvoltsMax = 5` (while expecting the `pvoltsMax = 1` instead). Again, regardless of whatever value such as 1, 2, 3 or 4 as the third parameter for the command `dwf.FDwfAnalogInChannelRangeSet()`, the result returned by `dwf.FDwfAnalogInChannelRangeInfo()` is always `pvoltsMax = 5`.

# Solutions

- 1. Solution for the **Problem - 1** (above),

  - 1.1 Mistake about the term **range** in the `dwf.FDwfAnalogInChannelRangeSet()` (i.e in sdk library):

    - **range** in the sdk library refers to **PEAK-TO-PEAK RANGE**. For example, if **range** is set the 5V, the maximum positive voltage could be recored/read-in by the oscill0scope is only 2.5V. That is why the positive/negative max amplitude is always 2.5V/-2.5V. This point is verified in [the discussion about similar problem 1 (above)](https://forum.digilent.com/topic/18231-waveforms-sdk-3115-data-aquisition-and-signal-generation-questions/s)

    - **range** in WaveForms application (i.e GUI provided by NI) has **totally different** meaning from **range** in the sdk library.

  - 1.2 why the setting of third parameter in `dwf.FDwfAnalogInChannelRangeSet()` with 1V, 2V, 3V or 4V always returns 5V in `dwf.FDwfAnalogInChannelRangeInfo()`?

    - according to this discussion about [range setting capability of the Analog Discovery 2 (which is similar to Analog Discovery 3)](https://forum.digilent.com/topic/18700-problem-setting-ch-2-voltage-range-ad2/) and ChatGPT further details on the explanation in the mentioned discussion, that because the Analog Discovery **ONLY** supports two ranges **either 5V or 50V**. The device (i.e the Analog Discovery) automatically decides which to use based on the value of the **third parameter** in  `dwf.FDwfAnalogInChannelRangeSet()`. If the **third parameter** is set to be any value less than 5V, then the range is automatically set to 5V in the device. If the **third parameter** is set to be any value bigger than 5V (such as 10V), then the range is automatically set to 50V in the device.

  - **Based on the point 1.1 and 1.2 above, the solution** is to set the **third parameter** in  `dwf.FDwfAnalogInChannelRangeSet()` to be bigger than 5V, so that the read-in amplitude of 4V or 3V (which makes the range to be 8V or 6V correpondingly) could be accomodate in the valid set range of 50V of Analog Discovery 3.