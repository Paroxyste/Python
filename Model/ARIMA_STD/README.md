# ARIMA STD

## Description
ARIMA STD is an automation of the ARIMA model (AutoRegressive Integrated Mobile Average) in order to be used via a CRON task _(automation)_ and to process time series in order to predict future behavior.

## Prerequisite

### Modules
- datetime
- numpy
- os
- pandas
- pickle
- re
- statsmodels
- sys

### CSV Format
- Format : 2D
- column 1 = datetime _(YYYY-mm-dd HH:MM:SS)_
- column 2 = valeurs

## Installation des Prérequis

```
# Launch the Python environment :
python3

# Installing Python modules via Pip
pip3 install -U numpy
pip3 install -U pandas
pip3 install -U statsmodels
```

```datetime``` ```os``` ```pickle``` ```re``` ```sys``` are available when installing Python.

## Usage

ARIMA STD requires 10 parameters at launch :

-  CSV_PATH <string>
-  CSV_NAME <string>
-  SEP <string>
-  TIME_RES <string>
-  DATE_START _(YYYY-MM-DD)_ <string>
-  TIME_START _(HH:MM:SS)_ <string>
-  DATE_STOP _(YYYY-MM-DD)_ <string>
-  TIME_STOP _(HH:MM:SS)_ <string>
-  MATRIX_DIR <string>
-  MATRIX_NAME <string>

#### Launch Script

**If python3 OR python2 is the only environment installed :**
```python
python ARIMA.py C:\Users\Administrateur\Documents\CSV_Folder\ mycsvname ; 15T 2020-06-18 12:30:00 2020-12-24 23:45:00 C:\Users\Administrateur\Documents\Output_Folder\ my_matrix
```

**If python2 AND python3 are installed :**
```python
python3 ARIMA.py C:\Users\Administrateur\Documents\CSV_Folder\ mycsvname ; 15T 2020-06-18 12:30:00 2020-12-24 23:45:00 C:\Users\Administrateur\Documents\Output_Folder\ my_matrix
```

#### Details :
```python
# CSV file
CSV_PATH = C:\Users\Administrateur\Documents\CSV_Folder\
CSV_NAME = mycsvname # Do not add the .csv extension

# Dataframe
SEP = ;
TIME_RES = 15T

# Timestamp
DATE_START = 2020-06-18
TIME_START = 12:30:00
DATE_STOP = 2020-12-24
TIME_STOP = 23:45:00

# Output file
MATRIX_DIR = C:\Users\Administrateur\Documents\Output_Folder\
MATRIX_NAME = my_matrix # Do not add the .txt extension.
```

#### Resample
The resampling must **obligatory** be in minutes in the form ```XXT``` example ```15T``` for 15 minutes.

#### Separator
- \t (tabs)
- \s (space)
- ,
- ;

## Model Fitting

```python
# ARIMA parameters
# model = ARIMA(df, order=(p, d, q))

# Default values
p = 2
d = 0
q = 2

# Maximum allowed values
p = 5
d = 2
q = 5
```

#### Testing Environment

- Python : 3.8.3
- Numpy : 1.18.5
- Pandas : 1.0.4
- StatsModels : 0.11.1