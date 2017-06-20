# OrchidReader Simple Setup

A python script intended to be an easy way to prepare runs of OrchidReader, the first step in the analysis chain for background data from HFIR.

## Overview
This program reads the contents of the given input directory and produces the files (OrchidReader configuration files and qsub batch files) necessary to run OrchidReader on the data. In that process it determines if it needs to break the data into several batches based on time gap between files, or if different files in the same folder belong to different array positions or detector configurations. It then outputs the appropriate sets of configuration files and qsub files in the output directory it was given (or the default output directory) and produces a script where it was run that will submit those batch processing files.

## Invocation
OrchidReaderSimpleSetup is invoked as follows:
```
orchid_reader_simple_setup.py <Path-To-Input-File-Directory> [Path-To-Output-File-Directory]
```
or
```
python orchid_reader_simple_setup.py <Path-To-Input-File-Directory> [Path-To-Output-File-Directory]
```

Here, `Path-To-Input-File-Directory` is the path to the directory containing the set of input files to be processed by OrchidReader. `Path-To-Output-File-Directory` is the path to the directory that individual batch outputs are to be placed in. It defaults to: `/data1/prospect/ProcessedData/OrchidAnalysis/TimeSeries_2017`, this default can be changed easily by modifying *orchid_reader_simple_setup.py* (the default is stored in the global variable: `DEFAULT_OUTDIR`).

## Adding New Configurations
Over the course of operation it is to be expected that the detector setup or array position can change, temporarily or otherwise, new detector configurations, array times, etc can be produced quite easily by editting serveral files.

### Adding a Detector Configuration Exception
For to add a detector configuration change for a small set of runs using a to a pre-existing configuration one need only edit *orsslib/setup_changes.py*.
  - Step 1: Add a new variable containing the patterns found in the file names from the runs for which the change applies. The example below describes runs for which only the moderated 3He detector was part of the setup.
  ```python
    MOD_HE_RUN_PATTERNS = ["Jun05_2017_0001.dat", "Jun06_2017_0000.dat"]
  ```
  - Step 2: Add the relevant detector setup to the end of the `EXCEPTION_DATA` list.
  ```python
    EXCEPTION_DATA = [ds.DEFAULT_SETUP, ds.CEBR_SETUP, ds.NO_HE_SETUP, ds.MOD_HE_SETUP]
  ```
  - Step 3: Add the name of the detector setup to the `EXCEPTION_NAME` list.
  ```python
    EXCEPTION_NAME = ["Default", "CeBr3", "No_3He", "Mod_3He"]
  ```
  - Step 4: Add the new list of file name patterns to the `EXCEPTION_PATTERN` variable.
  ```python
    EXCEPTION_PATTERN = [CEBR_RUN_PATTERNS, NO_HE_RUN_PATTERNS, MOD_HE_RUN_PATTERNS]
  ```
With these steps complete, any file names containing the patterns given in the variable in step 1, will have the detector setup set to the one given in `EXCEPTION_DATA`.

### Changing the Default Detector Configuration
To change the default detector configuration, simply change the first element of the `EXCEPTION_DATA` list to the new default detector configuration.

### Adding an Array Position Exception
To change the position that the array was in for a set of runs, follow a procedure similar to that for Adding a detector Configuration Exception with the following differences:
  - Edit *orsslib/position_changes.py* instead of *orsslib/setup_changes.py*
  - The entry in the `EXCEPTION_DATA` list is a tuple containing the x and y position of the array instead of a detector configuration class.

### Adding a New Detector Configuration
To add a new detector configuration, you need to edit *orsslib/detector_setups.py*.
  - First, create an array setup class and assign it to a new variable
   ```python
    NEW_SETUP = ArraySetup()
  ```
  - Second, create a detector setup class with the appropriate parameters. `electronic_config` is a tuple containing two tuples, the first tuple contains the digitizer module and channel number, the second tuple contains the MPOD HV system module and channel number. `position` is a tuple containing the x, y, and z offsets relative to the array position. `det_type` is a string containing the detector type, current options are: "NaI", "LS", "CeBr3", "HeMod", "HeUnmod". `thresholds` is a tuple containing energy and psd cutoff thresholds that should be applied to projections of that detectors spectra.
  ```python
    TMP = DetectorSetup(electronic_config, position, det_type, thresholds)
  ```
  - Third, add the detector to the array configuration. `detector_number` is the unique identifier for that particular detector.
  ```python
    NEW_SETUP.add_detector(detector_number, copy.deepcopy(TMP))
  ```
  - Fourth, repeat steps 2 and 3 for every detector in the array (copy, paste modify helps a lot).
