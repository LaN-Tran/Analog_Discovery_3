# Structure of folder 20250516

## Using WaveForms application provided by Digilent

- Demonstrating: setting up and measuring current, voltage of a diode

  - setting up AD3 and Diode: see `../README.md` - section `Reference` - [5] (of this Repository)

  - Setup the [`Wave generator`](https://digilent.com/reference/test-and-measurement/guides/waveforms-waveform-generator) and the ['Oscilloscope'](https://digilent.com/reference/test-and-measurement/guides/waveforms-oscilloscope) in the AD3

  - Start measuring and recording -> export `oscilloscope` result to `.csv` file 
    - **NOTE**:
      1. when exporting to `.csv` file, in order to make the file be readable by `pandas` library, the option `headers` - `comment` in WaveForms app must be **DE-SELECTED**. **The recorded `.csv` file is stored in the folder `../data/sample_test_Diode.csv`** 

  - Running the file `process_osc.ipynb` to plot the I/V curve of the measured Diode.

## Using SDK python to interact with the AD3 hardware instead of WaveForms application

- Simply open any IDE (e.g Vscode) with python installed, follow the instruction in this section to know how to use python to communicate with the hardware AD3 without using the WaveForms application provided by Digilent. Regardless of whether the WaveForms app is used or not, **WaveForms must be donwloaded and installed** to be able to use python for building a customed application to interact with AD3.

- **IMPORTANT**: **one hardware (AD3) - only one application connection**. 
    For example, before running codes in file `ad3_sdk_python.ipynb`, if the WaveForms application has been opened and runned; then, the code in file `ad3_sdk_python.ipynb` can not access the hardware AD3 anymore. That leads to failure as a result of running `ad3_sdk_python.ipynb` while WaveForms application has been opened to use already. 

- Before running `ad3_sdk_python.ipynb`, we must have physical measurement setup. **The simple setup for testing** is [AD3 W1/GND  - AD3 1+/1-](https://digilent.com/reference/test-and-measurement/analog-discovery-3/getting-started) = connect first wave generator of AD3 to the first Oscilloscope channel

- After downloading, linking the package **WF_SDK** (insruction in file `ad3_sdk_python.ipynb` - section `Workflow` - `3.Using Instruments`), and running the `ad3_sdk_python.ipynb` sucessfully, keeping the current measurement setup (AD3 W1/GND  - AD3 1+/1-), we could run the provided sample codes (`test_device_info.py`, `test_scope-wavegen.py`) in folder `../WaveForms-SDK-Getting-Started-PY-master/WaveForms-SDK-Getting-Started-PY-master` (which is the parent folder of the package **WF_SDK**. The folder is the result of the donwloading **WF_sDK** according to the  insruction in file `ad3_sdk_python.ipynb` - section `Workflow` - `3.Using Instruments`)

