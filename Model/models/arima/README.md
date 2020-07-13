# ARIMA

## Description
The estimation of ARIMA models assumes working on a stationary series. This means that the mean of the series is constant over time, as is the variance. The
The best method to eliminate any tendency is to differentiate, i.e. to replace the original series with the series of adjacent differences. A time series that needs to be differentiated to achieve stationarity is considered an integrated version of a stationary series.

## Prerequisite

**CSV format or via BDD :**

- Format : 2D
- column 1 = datetime _(YYYY-mm-dd HH:MM:SS)_
- column 2 = values

## Usage

PROPHET requires a configuration file :
- CONFIG_FILE

### Launch Script

**Python 3 :**
```python
python3 run_arima.py C:\Users\Administrateur\Documents\Config\config_file.txt
```

**Python 2 :**
```python
python run_arima.py C:\Users\Administrateur\Documents\Config\config_file.txt
```

### Details :
```python
# Config file
CONFIG_FILE = C:\Users\Administrateur\Documents\Config\config_file.txt
```

## Config File

```python
[DATA]

date_start : 2020-01-01 00:00:00
date_stop  : 2020-08-01 12:00:00

[ARIMA]

p : 2
d : 0
q : 2

```

## Model Fitting

```python
# min : 2
# max : 5 
# default : 2
p : 2

# min : 0
# max : 2
# default : 0
d : 0

# min : 2
# max : 5
# default : 2
q : 2

# Start of prediction (this value influences the training of the model)
date_start : 2020-01-01 00:00:00

# End of the prediction
date_stop  : 2020-08-01 12:00:00
```