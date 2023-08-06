[![ci-cd](https://github.com/UBC-MDS/Group28-CovidTracker/workflows/ci-cd/badge.svg)](https://github.com/UBC-MDS/Group28-CovidTracker/actions)
[![codecov](https://codecov.io/gh/UBC-MDS/Group28-CovidTracker/branch/main/graph/badge.svg?token=tKi5DL8bCF)](https://codecov.io/gh/UBC-MDS/Group28-CovidTracker)
[![Documentation Status](https://readthedocs.org/projects/covidtracker/badge/?version=latest)](https://covidtracker.readthedocs.io/en/latest/?badge=latest)


# covidtracker

Provides basic data cleaning, wrangling and plotting of Covid tracking data in Canada.

## Functions
The covidtracker package is designed for the easy retrieval and analysis of data pertaining to Covid trends in Canada, including information about cases, vaccinations and testing. The package serves as a wrapper for the opencovid.ca [API](Ihttps://opencovid.ca/api/), and provides additional helper functions for visualising the data, either as a time series or in the form of a map. 

* #### `get_covid_data()`
    Retrieve cleaned and formatted data of specified type and within (optionally) provided time ranges and locations

* #### `plot_time_series()`
    Function for plotting time series trends in Covid data

* #### `calculate_stat_summary()`
    Function for returning key statistical information about Covid data, such as long run trends and comparisons between provinces<br>

* #### `plot_geographical()`
    Function for plotting chloropleth maps with Covid data 
    

## Similar Packages    
There are currently no other Python packages available that can perform the same set of data retrieval and analysis functionalities as covidtracker. There are several packages that have similar functionality, but are most are tailored either towards covid data retrieval or data visualization. The packages designed for covid data retrieval also do not use the same data source as covidtracker. Some examples of related Python packages useful for Covid data retrieval and data visualizations include:
* [covid19dh](https://pypi.org/project/covid19dh/) - For Covid data retrieval
* [covid](https://pypi.org/project/covid/)- For Covid data retrieval
* [folium](https://pypi.org/project/folium/) - For data visualizations
* [plotly](https://pypi.org/project/plotly/) - For data visualizations


## Installation
Please note that due to GDAL dependencies, the package can only be directly installed on Mac OS and Linux machines. With Windows machine, because `pip install Fiona` does not work, you need to install Fiona package first, and then install our covidtracker package.

Mac OS and Linux machine:
```bash
$ pip install covidtracker
```

Windows machine:
```bash
$ conda install Fiona
$ pip install covidtracker
```

## Usage

```python
from covidtracker.get_covid_data import get_covid_data
from covidtracker.plot_geographical import plot_geographical
from covidtracker.plot_time_series import plot_ts
from covidtracker.calculate_stat_summary import calculate_stat_summary

covid_df = get_covid_data('active')
head(covid_df)
```
![alt text](https://github.com/UBC-MDS/Group28-CovidTracker/blob/main/figures/get_covid_data.PNG?raw=true)

```python
covid_df = get_covid_data()
plot_geographical(covid_df, 'cases')
```
![alt text](https://github.com/UBC-MDS/Group28-CovidTracker/blob/main/figures/plot_geographical.PNG?raw=true)


```python
plot_ts(covid_df,"cases")
```
![alt text](https://github.com/UBC-MDS/Group28-CovidTracker/blob/main/figures/plot_ts.PNG?raw=true)


```python
summary = calculate_stat_summary(covid_df, 'cases')
```
![alt text](https://github.com/UBC-MDS/Group28-CovidTracker/blob/main/figures/summary.PNG?raw=true)

## Documentation
Detailed documentation for the package can be found here on Read the Docs : https://covidtracker.readthedocs.io/en/latest/ 

## Contributing

We welcome and recognize all contributions. Please see contributing guidelines in the Contributing document. This repository is currently maintained by

* Cuthbert Chow (@cuthchow)
* Tianwei Wang (@Davidwang11)
* Siqi Tao (@SiqiTao)
* Jessie Wong (@jessie14)

## License

`covidtracker` was created by Group 28. It is licensed under the terms of the MIT license.

## Credits

`covidtracker` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).
