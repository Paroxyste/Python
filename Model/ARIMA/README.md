# ARIMA

## Description
The estimation of ARIMA models assumes working on a stationary series. This means that the mean of the series is constant over time, as is the variance. The
The best method to eliminate any tendency is to differentiate, i.e. to replace the original series with the series of adjacent differences. A time series that needs
to be differentiated to achieve stationarity is considered as an integrated version of a stationary series.

## Prerequisite

**Format CSV :**

- Format : 2D
- column 1 = datetime _(YYYY-mm-dd HH:MM:SS)_
- column 2 = valeurs

## Usage

ARIMA requires 7 parameters at launch:

-  CSV_DATA
-  DATE_START _(YYYY-MM-DD)_
-  TIME_START _(HH:MM:SS)_
-  DATE_STOP _(YYYY-MM-DD)_
-  TIME_STOP _(HH:MM:SS)_
-  MATRIX_OUTPUT
-  CONFIG_FILE

### Script Launch

**If python3 OR python2 is the only environment installed :**
```python
python run.py C:\Users\Administrateur\Documents\CSV_Folder\mycsvname.csv 2020-06-18 12:30:00 2020-12-24 23:45:00 C:\Users\Administrateur\Documents\Output_Folder\my_matrix.txt C:\Users\Administrateur\Documents\Config\config_file.txt
```

**If python2 AND python3 are installed :**
```python
python3 run.py C:\Users\Administrateur\Documents\CSV_Folder\mycsvname.csv 2020-06-18 12:30:00 2020-12-24 23:45:00 C:\Users\Administrateur\Documents\Output_Folder\my_matrix.txt C:\Users\Administrateur\Documents\Config\config_file.txt
```

### Details :
```python
# CSV file
CSV_DATA = C:\Users\Administrateur\Documents\CSV_Folder\myCSV.csv

# Timestamp
DATE_START = 2020-06-18
TIME_START = 12:30:00
DATE_STOP = 2020-12-24
TIME_STOP = 23:45:00

# Output file
MATRIX_OUTPUT = C:\Users\Administrateur\Documents\Output_Folder\my_matrix.txt

# Config file
CONFIG_FILE = C:\Users\Administrateur\Documents\Output_Folder\config_file.txt
```

## Resample
The resampling must **obligatory** be in minutes in the form ```XXT``` example : ```15T``` for 15 minutes.

- The default setting is : **15T**

## Separator
- \t (tab)
- \s (space)
- ,
- ;

- The default setting is : **;**

## Model Fitting

```python
# Maximum allowed values
p = 5
d = 2
q = 5
```

- The default settings of these parameters are : **p = 2 | d = 0 | q = 2**

## Config File

```
[ARIMA]

separator : ;
resampler : 15T

p : 2
d : 0
q : 2
```

## Test Environment

- Python : 3.8.3
- Numpy : 1.18.5
- Pandas : 1.0.4
- StatsModels : 0.11.1