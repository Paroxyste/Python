# Available functions

**clean_data**
>
> Format the datetime as YYYY-mm-dd HH:TT:SS
>
> Cleans up missing values.
>
> **Parameter :** ```df```
>
> - _This function requires the installation of : [pandas](https://pandas.pydata.org/docs/getting_started/index.html#getting-started)_

---

**[csv-to-influxdb](https://github.com/fabio-miranda/csv-to-influxdb)**
>
> Loads a data file into influxDB.
>
> ```python3 csv-to-influxdb.py --dbname test --input data.csv --tagcolumns computer --fieldcolumns value```
>
> - _This function uses the modules ```argparse``` ```csv``` ```datetime``` ```gzip``` of python_
> 
> - _This function requires the installation of : [requests](https://requests.readthedocs.io/en/master/) - [pytz](https://pythonhosted.org/pytz/) - [influxdb-python](https://influxdb-python.readthedocs.io/en/latest/include-readme.html)_

---

**load_data_influx**
>
> Retrieves a metric from the InfluxDBClient using an SQL query, and transforms the data into a DataFrame.
>
> This function also integrates the [clean_data]().
>
> **Parameters :** ```server_name``` ```server_port``` ```user_name``` ```user_pass``` ```db_name``` ```request```
>
> - _This function requires the installation of : [influxdb-python](https://influxdb-python.readthedocs.io/en/latest/include-readme.html) - [pandas](https://pandas.pydata.org/docs/getting_started/index.html#getting-started)_

---

**make_folder**
>
> Create a folder.
>
> **Parameter :** ```path```
>
> - _This function uses the modules ```os``` of python_

---

**read_params**
>
> Allows you to retrieve the meters from a config file.
>
> **Parameters :** ```config``` ```section``` ```parameter``` ```default```
>
> - _This function uses the modules ```configparser``` of python_

---


**save_data**
>
> Exports a DataFrame to a text file.
>
> **Parameters :** ```data``` ```data_name``` ```path_file```
>
> - _This function requires the installation of : [pandas](https://pandas.pydata.org/docs/getting_started/index.html#getting-started)_

---

**ts_generator**
>
> Generates a time series.
>
> **Parameters :** ```date_start``` ```date_stop```
>
> - _This function uses the module ```datetime``` of python_
> 
> - _This function requires the installation of : [numpy](https://numpy.org/install/)_