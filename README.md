# FIZEMO

This program is designed to process physiological signals and extract the most important features from them.
For more details check [Detailed description](#detailed-description)


## A research project created by 

  Kasia Kaczorowska 

  Karolina Bednarska

  Maciej Szarecki

  Iwo Brzyski
  

## Packages needed before program execution
**Recomended python version**: 3.8.9

If you are using pip, you can try this snippets:
   * matplotlib
    
    pip install matplotlib
    
   * scipy
    
    pip install scipy
    
   * numpy
    
    pip install numpy

   * pandas
    
    pip install pandas
  
   * stat
    
    pip install stat
    
   * peakutils
    
    pip install peakutils
    
   * peakutils
    
    pip install peakutils

   * pyhrv
    
    pip install pyhrv
    
   * biosppy
    
    pip install biosppy

    
## HOW TO INSTALL AND RUN THE PROGRAM
   1. Clone the program
    
    git clone https://github.com/FIZEMO/FIZEMO.git
  2. Install all the necessary dependencies contained in [Detailed description](#packages-needed-before-program-execution) section.
  3. Customize the `config.json` file in the `./configuration` catalog according to your needs: you will find how to do this in the following sections.
  4. Put the signals you want to process as csv files into the `./signals` folder
  5. How to run the program:
      - If one runs program from developer tool like PyCharm:
        1. Set configuration parameter (command line parameters) as the path to configuration file (For PyCharm: Run->Edit Configurations and write in Parameters field the path to configuration file, for example "./configuration/config.json")
      - If one runs program from command line (for Windows users):
          1. Start Command Line and set path to the location where the main program is located (example C:\Documents\Projects\FIZEMO)
          2. Run main program with one attribute - the relative path to configuration file:
    
    py -3 main.py "./configuration/config.json"
    
    
**Results**: After successful run of the program you will find extracted features in `./results/features` catalog, and processed signal in `./results/signals` folder in files with the same name as you named the scenario. If you include more than one scenario in the configuration file, you will have more output files in those folders.
    
## Detailed description
Here are presented all the functions that can be used during signal processing.
Configuration file is a JSON file, which consists of flow scenarios for one signal. Each scenario has its own signal
processing flow (preprocessing methods and feature extraction order).
For each method there is a special name and attributes names that must be used and signed in configuration file.
For each feature extraction there is a special name that must be used and signed in configuration file.

This program gives complete freedom to the user so one can create many processing scenarios,
and each of them can be given any name. What is more, in each scenario many processing methods can be used in any order,
and one processing method can be used more than once in the single scenario.

As the result, for each scenario user receives .csv files which contains:
* extracted features from processed signal
    - only if at least one feature was specified in the scenario *(file placed in ./results/features/ directory).*
*  signal after all modifications and running processing methods *(file placed in ./results/signals/ directory).*

If you're feeling overwhelmed by the possibilities, take a look at the sample configuration file, and I'm
sure things will lighten up :bulb:.

***Examples of configuration files are placed in  ./configuration folder.***


## SCENARIO STRUCTURE
Each scenario defined in configuration file has a special structure. 
### It has to contain four elements:
  - `"signalFileName"` - a string representing the name of the file with signal which is placed in ./signals catalog 
     > *example: "./signals/rawGSR"*
  - `"signalType"` - a string representing a type of processed signal, it has to be chosen from the list of [available types of signal](#available-types-of-signal).
  - `"methods"` - list of methods for signal processing or feature extraction
  - `"columns_to_read"` - dictionary which contains information about columns to read from .csv file with signal data with specified "timestamp" column number and "values" column number

### There are two optional elements:
  - `"options"` - dictionary which may contain two elements (both optional):
    * `"save_processed_signal"` - if set to "False" the program doesn't save the .csv file with processed signal; if this field is not specified, the default value is "True"
    * `"draw_plot"` if set to "False" the program doesn't plot the processed signal; if this field is not specified, the default value is "True"
  - `"windowing_attr"` - dictionary which contains:  
    ***IMPORTANT: Not available for ECG signal yet - will come in future patches.***
    * `"length"` - the length of the window
    * `"slide"` - the slide of the window (windows can overlap)

**Example:**
```json
{
  "Scenario for GSR": [
      {
        "signalFileName": "rawGSR",
        "signalType": "GSR",
        "columns_to_read": {"timestamp": 1, "values": 2},
        "options": {
          "draw_plot": "False"
        },
        "windowing": {"length": 1000, "slide": 500},
        "methods": [
          {
            "functionName": "decimate",
            "order": 1,
            "attributes": {
              "samplingFrequency": 128,
              "goalFrequency": 50
            }
          },
          {
            "functionName": "maximum",
            "order": 2,
            "outputLabel": "Max"
          }
        ]
      }
    ],
    "Scenariusz for ECG": [
    {
      "signalFileName": "rawECG",
      "signalType": "ECG",
      "columns_to_read": {"timestamp": 1, "values": 2},
      "methods": [
        {
          "functionName": "pan_tompkins",
          "order": 1,
          "attributes": {
            "filterOrder": 5,
            "samplingRate": 250,
            "cutOfFrequencies": [
              5,
              15
            ],
            "lengthOfWindow": 15
          }
        },
        {
          "functionName": "get_poincare_parameters",
          "order": 2
        },
      ]
    }
  ]
}
```

## AVAILABLE TYPES OF SIGNAL
  - GSR (Galvanic Skin Response)
  - ECG (Electrocardiography)

## PROCESSING METHOD STRUCTURE 
We call methods for processing signal inside `"methods"` array inside config file.
To call function for processing signal in configuration file one has to fill 3 elements:
  - `"functionName"`: "..." - the name of the function one wants to use (string),
  - `"order"`: ... - natural number bigger or equal 1 which indicates the order of processing flow (int),
  - `"attributes"`: { #attributes } - attributes that are unique for each function; they specify function parameters. For some functions this element might be omitted (for example look at [Z NORMALIZATION](#z-normalization) function).

**Example for method that filter the signal with butterworth filter:**
```json
"methods": [
  {
    "functionName": "butterworth_filter",
    "order": 1,
    "attributes": {
      "filterOrder": 5,
      "samplingRate": 250,
      "type": "bandpass",
      "cutOfFrequencies": [
        5,
        15
      ]
    }
  },
  {
    "functionName": "z_normalize",
    "order": 2
  }
]
```

## AVAILABLE METHODS
### AVAILABLE FOR BOTH GSR and ECG signals:
#### [BUTTERWORTH FILTER]
  - Description:  Filter the signal with butterworth filter
  - Function name: `"butterworth_filter"`
  - Attributes:
    - `"samplingRate"` - signal sampling rate/frequency (integer - [Hz])  
        **REMEMBER**: If you have used decimation function, you should type in sampling rate you achieved after decimation process!
    - `"filterOrder"` - the order of filter that will be created (integer - [Hz])
    - `"type"` - the type of the filter. Available types (string):
        'lowpass',
        'highpass'
        'bandpass'
        'bandstop'
    - `"cut_of_freq"` it is an array or a scalar of cut of frequencies.
        Scalar for 'lowpass' and 'highpass' filter (float - [Hz]). Example: 5.0
        Array of two values for 'bandpass' and 'bandstop' filter ([float, float] - [Hz]). Example: [5.0, 15.0]

#### [DIFFERENTIATE]
  - Description: Differentiate the signal
  - Function name: `"differentiate"`
  - Attributes: None

#### [SQUARE]
  - Description: Squares every value of the signal
  - Function name: `"square"`
  - Attributes: None

#### [MOVING WINDOW INTEGRATION]
  - Description:  Integrate the signal with moving frame of the given length
  - Function name: `"moving_window_integration"`
  - Attributes:
      - `"lengthOfWindow"`: length of the moving window (integer - number of samples)

#### [DECIMATION]
 - Description:  process of bandwidth reduction (filtering) and sample-rate reduction
 - Function name: `"decimate"`
 - Attributes:
    - `"samplingFrequency"` - frequency with which signal was sampled (integer - [Hz])
    - `"goalFrequency"` - goal frequency with which signal should be sampled (integer - [Hz])

#### [GET PHASE PART]
  - Description:  calculate phase part of given signal by subtract baseline values
  - Function name: `"get_phase_part"`
  - Attributes:
    - `"deg"` is degree of the polynomial that will estimate the data baseline - *recommended is 10*
    - `"maxIt"` is maximum number of iterations to perform for baseline function - *recommended is 100*

#### [Z NORMALIZATION]
  - Description:  process of normalizing signal by its standard deviation
  - Function name: `"normalize_by_std"`
  - Attributes: None

#### [SMOOTH]
  - Description: Smooths out the signal by averaging the samples.
  - Function name: `"smooth"`

### AVAILABLE ONLY FOR ECG signals:

#### [PAN TOMPKINS]
   - Description: Uses Pan–Tompkins algorithm to extract vector of R-peaks distances.  
    In this solution following steps are being executed:  
      1. Filter signal with bandpass filter, where user can choose:
          - cut of frequencies: *recommended [5, 15]*
          - order of the filter
      2. Differentiate the signal.
      3. Square the signal.
      4. Applies moving window integration, where user use can chooose:
          -length of the moving window.
      5. Calculate vector with R-peaks distances

  - **IMPORTANT**: This method must be executed before the following methods:
    - get_vector_r_peaks_distance_parameters
    - get_poincare_parameters  
  - Function name: `"pan_tompkins"`
  - Attributes:
     - `"samplingRate"` - signal sampling rate/frequency (integer - [Hz])  
          **REMEMBER**: If you have used decimation function, you should type in sampling rate you achieved after decimation process!
     - `"filterOrder"` - the order of filter that will be created (integer - [Hz])
     - `"cut_of_freq"` it is an array of cut off frequencies.  
          Array of two values  ([float, float] - [Hz]). Example: [5.0, 15.0]
     - `"lengthOfWindow"`:
          length of the moving window (integer - number of samples)  

## FEATURE EXTRACTION METHOD STRUCTURE
We call methods for feature extraction identically like we would call method for processing signal, which is inside `"methods"` array inside config file.
To call function for feature extraction from the signal in configuration file one has to fill 3 elements:
  - `"functionName"`: "..." - name of the function one wants to use (string),
  - `"order"`: ... - natural number bigger or equal 1 which indicates the order of processing flow (int),
  - "outputLabel": "..." - optional elements where user can define label for extracted feature. (string)
    If this element is omitted, program will generate default output label for a feature.
    Otherwise, the label will be exactly the same as specified in the configuration file.
    
**Example for method that extracts standard deviation from the signal:**
"methods": [
  {
    "functionName": "standard_deviation",
    "order": 1,
    "outputLabel": "Std"
  },
  {
    "functionName": "maximum",
    "order": 2
  }
]

## AVAILABLE METHODS FOR FEATURE EXTRACTION
### AVAILABLE FOR BOTH GSR and ECG signals:
#### [MEAN]
  - Description: Function to extract mean value from the signal
  - Function name: `"mean"`
  - Default output label: "Mean"

#### [MEDIAN]
  - Description: Function to extract median value from the signal
  - Function name: `"median"`
  - Default output label: "Median"

#### [STANDARD DEVIATION]
  - Description: Function to extract standard deviation value from the signal
  - Function name: `"standard_deviation"`
  - Default output label: "Standard deviation"

#### [MINIMUM]
  - Description: Function to extract minimum value from the signal
  - Function name: `"minimum"`
  - Default output label: "Minimum"

#### [MAXIMUM]
  - Description: Function to extract maximum value from the signal
  - Function name: `"maximum"`
  - Default output label: "Maximum"

#### [VARIANCE]
  - Description: Function to extract the variance value from the signal
  - Function name: `"variance"`
  - Default output label: "Variance"

#### [KURTOSIS]
  - Description: Function to extract kurtosis value from the signal
  - Function name:`"kurtosis"`
  - Default output label: "Kurtosis"

#### [SKEWNESS]
  - Description: Function to extract skewness value from the signal
  - Function name: `"skewness"`
  - Default output label: "Skewness"

#### [AREA UNDER CURVE]
  - Description: Function to extract the area under the curve characteristic value from the signal.
  - Function name: `"area_under_curve"`
  - Default output label: "Area under curve"

### AVAILABLE ONLY FOR ECG signals:

#### [GET VECTOR R PEAKS DISTANCE PARAMETERS]
  - Description:  Extract mean, standard deviation, heart rate and RMSSD of distance R vector.
  - Function name: `"get_vector_r_peaks_distance_parameters"`
  - Attributes: None

#### [GET POINCARE PARAMETERS]
  - Description: Extract SD1 and SD2 values from poincare plot.
  - Function name: `"get_poincare_parameters"`
  - Attributes: None

#### [GET PSD PARAMETERS]
  - Description: Extract LF HF, their normalized values and ratio LF/HF.
  - Function name: `"get_psd_parameters"`
  - Attributes: None
