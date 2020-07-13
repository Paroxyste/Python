# Analyse Supervision

## Modèles

**ARIMA**
>
> The model attempts to determine each value in the series based on the values that precede it.  
> ARIMA model estimation assumes a stationary series. 
> This means that the mean of the series is constant over time, as is the variance.
> 
> - _This model requires the installation of [statsmodels](https://www.statsmodels.org/stable/index.html)._

---

**PROPHET**
>
> Prophet is a tool for producing high quality forecasts for time series data with 
> multiple seasonality with linear or non-linear growth.
>
> - _This model requires the installation of [fbprophet](https://facebook.github.io/prophet/docs/quick_start.html)._

---

## Fonctions

- clean_data
- [csv-to-influxdb](https://github.com/fabio-miranda/csv-to-influxdb)
- load_data_influx
- make_folder
- read_params
- save_data
- ts_generator

---