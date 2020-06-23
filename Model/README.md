# Analyse Supervision

## Modèle disponible
**ARIMA**
>
> The model attempts to determine each value in the series based on the values that precede it. ARIMA model estimation assumes a stationary series. This means that the mean of the series 
> is constant over time, as is the variance.
> 
> - _This function requires the installation of StatsModels._

## Fonctions disponible
**datetime_index**
> 
> Generates an index by taking a start date and time ```DATE_START``` ```TIME_START```, an end date and time ```DATE_STOP``` ```TIME_STOP```, and a time interval ```resampler```.


**extract_data**
>
> Retrieves the prediction matrix of the model to train ```model_fit``` from a start date and time ```DATE_START``` ```TIME_START```, and a date and time of end ```DATE_STOP``` 
> ```TIME_STOP```.


**loading_data**
> 
> Loads the data from a file and its path ```CV_DATA```, processes it via a given separator ```separator``` and is then ```resampled```. It includes also functions for cleaning up missing > values.
>
> - _This function requires the installation of Pandas_


**matrix_2d**
>
> Transforms the columns created via the functions ```extract_data()``` and ```datetime_index()``` to recreate a 2-dimensional output matrix.
> 
> - _This function requires the installation of Numpy_


**read_params**
> 
> Allows you to retrieve the parameters from a config file.


**save_data**
> 
> Exports the matrix in text format, created from the 2D table ```new_matrix``` of the function ```matrix_2d()``` at a given location ```MATRIX_OUTPUT```.
> 
> - _This function requires the installation of Numpy_
