# Reference

- [1] Cross-triggering (device to device, or instrument to instrument (wavegen triggers oscilloscope) within the same device):

  - 1.1 [Python sdk trigger](https://github.com/LaN-Tran/Analog_Discovery_3/blob/main/WaveSDK_examples/AnalogInOut_Trigger.py)

  - 1.2 [WaveForms software, cross-trigger setup](https://digilent.com/reference/test-and-measurement/guides/waveforms-cross-triggers?srsltid=AfmBOooMMRwx_cBVjlW5bj9ukmPpigvzxYXIOSZxdVumdQnouqidb_S5)

- [2] WaveForms application reference:

  - 2.1 [General reference](https://digilent.com/reference/software/waveforms/waveforms-3/reference-manual)

  - 2.2 Details reference: WaveForms app installation path (such as, `C:/Program Files (x86)/Digilent`) -> `WaveForms3/doc/index.html`

- [3] [Youtube video, ](https://www.youtube.com/watch?v=-EPb40jpdl4)

# Comments about things in the reference

- In [2], section 7 - Triggers:

  - "button under the main window device menu" = "Manual Trigger" in the Waveform app (Correct, see the [2.2] - section 7- Triggers and compared with [2] - section 7 - Triggers) = The trigger PC event = In WaveForms app, Wavegen, **Trigger: Manual**

- According to [3], (I think similar to Analog Discovery 3 device), the device can be powered by the USB cable (to the computer/ power bank) or the socket power (if only, we need higher range of generated power supply from the device) 

- 