# Folder description

- 1. `AnalogIn_Record.py`

  - A modification of the Digilent example (whose name is the same). Modification includes:

    - plot the live recorded signal.

    - Add some debug functions to understand the `cAvailable` returned from `dwf.FDwfAnalogInStatusRecord(hdwf, byref(cAvailable), byref(cLost), byref(cCorrupted))`

- 2. `measurement_prac2.ipynb`

  - Including experiments:
  
    - EXP 1: 
    
     - Test of independently control of each wave generator channels. Also, controlling them together, for example, both turning them on at the same time.
    
     - Test the control of how to output number of periods of a periodic signal from each wave channel. 
