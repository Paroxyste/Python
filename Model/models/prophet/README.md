# PROPHET

## Description
The FB Prophet model, implements a forecasting procedure for time series data based on an additive model where non-linear 
trends are fitted to annual, weekly and daily seasonality and the effects of holidays. It works best with time series that 
have strong seasonal effects and a data history of several years.

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
python3 run_prophet.py C:\Users\Administrateur\Documents\Config\config_file.txt
```

**Python 2 :**
```python
python run_prophet.py C:\Users\Administrateur\Documents\Config\config_file.txt
```

### Details :
```python
# Config file
CONFIG_FILE = C:\Users\Administrateur\Documents\Config\config_file.txt
```

## Config File

```python
[PROPHET]

days : 7
freq : 'T'

initial : '42 days' # initial = horizon * 2
period  : '7 days'  # period  = days
horizon : '21 days' # horizon = period * 3 

```

## Model Fitting

```python
# Max values of the prediction (in days)
days = 7

# Frequency of each prediction
# Years   = 'Y'
# Months  = 'm'
# Days    = 'd'
# Hours   = 'H'
# Minutes = 'T'
# Seconds = 'S'
freq = 'T'

# Example for the above settings :
#                  ds yhat
# 2020-01-01 00:01:00 0.1
# 2020-01-01 00:02:00 0.5
# 2020-01-01 00:03:00 0.3
# ...
# 2020-01-08 23:57:00 0.7
# 2020-01-08 23:58:00 0.2
# 2020-01-08 23:59:00 0.9
```