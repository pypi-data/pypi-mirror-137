# pystockwatch

[![codecov](https://codecov.io/gh/UBC-MDS/pystockwatch/branch/main/graph/badge.svg?token=c6vEGpbs3h)](https://codecov.io/gh/UBC-MDS/pystockwatch)
[![build](https://github.com/UBC-MDS/pystockwatch/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/UBC-MDS/pystockwatch/actions/workflows/ci-cd.yml)
[![Documentation Status](https://readthedocs.org/projects/pystockwatch/badge/?version=latest)](https://pystockwatch.readthedocs.io/en/latest/?badge=latest)


This package has been created to provide a very simple interface for checking movements in stock prices in comparison to the market. This is implemented by accessing public data from Yahoo Finance by selecting a ticker of the stock, range of start and end dates and benchmark for comparison, such as `SP500` or `NASDAQ`. As a result of data processing with pystockwatch package, users will be able to generate two plots: one with two lines showing percentage change in profit since the start date and volumes of trading and another related to daily change in the volume of stock trades as shown at examples below

 
 #### Functions description
 
 This package is built with following four functions:
 - `percent_change`
 Calculation of profit percentage change of a stock for a given period of time based on data extracted from Yahoo finance.
 - `profit_viz`
 Visualization of profit percentage change trend of a stock against market benchmark for a given period of time. Note that during weekends and public holidays, stock market has no data available, this is handled in plotting as well  
 - `volume_change`
 Calculation of daily trading volume change of a stock, whether it is increasing or decreasing. This data is used in  next function for color mapping of bar plot.
 - `volume_viz`
 Visualization of trading volume as bar plots colored by changes in volume in comparison with previous day. This plot is overlayed with line plots created with the second function. . Note that during weekends and public holidays, stock market has no data available, this is handled in plotting as well  
  
 More information about those functions can be found in docstrings of `/src/pystockwatch/pystockwatch.py`.
 
#### Comparison with similar packages
There are many packages written for analysis of stock data. One of the most popular Python package in this category is `pyti`, which gives a lot of manipulations with time series data, such as creating moving averages of stock price or calculating hundreds of parameters for technical analysis. Power of `pystockwatch` is in its simplicity, so users are not overwhelmed with all extra features and just have a simple view with key comparisons for a stock of interest.

## Installation

```bash
$ pip install pystockwatch
```

## Usage
After the sucessful installation of this package user will be required to input four parameters: `stock_ticker`, `start_date`, `end_date` and `benchmark_ticker`. Output results will be in form of an interactive plot based on "plotly" and "altair" package.

`pystockwatch` can be used to find the profit percent of stock prices in comparison to the market and check the trend in volume change of stocks and plot results as follows:

Import the functions from package with following commands:

```python
from pystockwatch.pystockwatch import percent_change
from pystockwatch.pystockwatch import profit_viz
from pystockwatch.pystockwatch import volume_change
from pystockwatch.pystockwatch import volume_viz
```
### To check the Profit percent

```
percent_change('AAPL', '2017-01-01', '2017-01-10')
```

### To Visualize the profit percentage change trend of a stock against market benchmark

```
fig = profit_viz('AAPL', '2015-01-01', '2021-12-31', 'SPY')
fig.show()
```
![**Percent Change**](https://github.com/UBC-MDS/pystockwatch/blob/main/docs/percent_change_example.png?raw=true)

### To check daily trading volume change of a stock

```
volume_change('AAPL', '2021-01-01', '2022-01-01')
```
### To Visualize the volume change trend of a stock 

```
vol = volume_viz('AAPL', '2021-01-01', '2022-01-01')
vol.show()
```
 ![**Volume Change**](https://github.com/UBC-MDS/pystockwatch/blob/main/docs/volume_plot_example.png?raw=true)

## Documentation

The documentation of this package is hosted on Read the Docs: [here](https://pystockwatch.readthedocs.io/)

## Contributors

* Affrin Sultana
* Helin Wang
* Pavel Levchenko
* Shi Yan Wang

## Contributing

Are you interested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

## Dependencies
Before the installation of this package please install the following packages:

* python = "^3.9"
* pandas = "^1.3.5"
* altair = "^4.2.0"
* altair_viewer = "^0.4.0"
* pandas-datareader = "^0.10.0"

## License

`pystockwatch` was created by Affrin Sultana, Helin Wang, Pavel Levchenko, Shi Yan Wang.It is licensed under the terms of the MIT license. 

## Credits

`pystockwatch` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).
