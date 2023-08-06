# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pystockwatch']

package_data = \
{'': ['*']}

install_requires = \
['altair-viewer>=0.4.0,<0.5.0',
 'altair>=4.2.0,<5.0.0',
 'pandas-datareader>=0.10.0,<0.11.0',
 'plotly>=5.5.0,<6.0.0',
 'yfinance>=0.1.69,<0.2.0']

setup_kwargs = {
    'name': 'pystockwatch',
    'version': '0.3.4',
    'description': 'A package which calculates and visualizes the profitability and the volume change of stocks ',
    'long_description': '# pystockwatch\n\n[![codecov](https://codecov.io/gh/UBC-MDS/pystockwatch/branch/main/graph/badge.svg?token=c6vEGpbs3h)](https://codecov.io/gh/UBC-MDS/pystockwatch)\n[![build](https://github.com/UBC-MDS/pystockwatch/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/UBC-MDS/pystockwatch/actions/workflows/ci-cd.yml)\n[![Documentation Status](https://readthedocs.org/projects/pystockwatch/badge/?version=latest)](https://pystockwatch.readthedocs.io/en/latest/?badge=latest)\n\n\nThis package has been created to provide a very simple interface for checking movements in stock prices in comparison to the market. This is implemented by accessing public data from Yahoo Finance by selecting a ticker of the stock, range of start and end dates and benchmark for comparison, such as `SP500` or `NASDAQ`. As a result of data processing with pystockwatch package, users will be able to generate two plots: one with two lines showing percentage change in profit since the start date and volumes of trading and another related to daily change in the volume of stock trades as shown at examples below\n\n \n #### Functions description\n \n This package is built with following four functions:\n - `percent_change`\n Calculation of profit percentage change of a stock for a given period of time based on data extracted from Yahoo finance.\n - `profit_viz`\n Visualization of profit percentage change trend of a stock against market benchmark for a given period of time. Note that during weekends and public holidays, stock market has no data available, this is handled in plotting as well  \n - `volume_change`\n Calculation of daily trading volume change of a stock, whether it is increasing or decreasing. This data is used in  next function for color mapping of bar plot.\n - `volume_viz`\n Visualization of trading volume as bar plots colored by changes in volume in comparison with previous day. This plot is overlayed with line plots created with the second function. . Note that during weekends and public holidays, stock market has no data available, this is handled in plotting as well  \n  \n More information about those functions can be found in docstrings of `/src/pystockwatch/pystockwatch.py`.\n \n#### Comparison with similar packages\nThere are many packages written for analysis of stock data. One of the most popular Python package in this category is `pyti`, which gives a lot of manipulations with time series data, such as creating moving averages of stock price or calculating hundreds of parameters for technical analysis. Power of `pystockwatch` is in its simplicity, so users are not overwhelmed with all extra features and just have a simple view with key comparisons for a stock of interest.\n\n## Installation\n\n```bash\n$ pip install pystockwatch\n```\n\n## Usage\nAfter the sucessful installation of this package user will be required to input four parameters: `stock_ticker`, `start_date`, `end_date` and `benchmark_ticker`. Output results will be in form of an interactive plot based on "plotly" and "altair" package.\n\n`pystockwatch` can be used to find the profit percent of stock prices in comparison to the market and check the trend in volume change of stocks and plot results as follows:\n\nImport the functions from package with following commands:\n\n```python\nfrom pystockwatch.pystockwatch import percent_change\nfrom pystockwatch.pystockwatch import profit_viz\nfrom pystockwatch.pystockwatch import volume_change\nfrom pystockwatch.pystockwatch import volume_viz\n```\n### To check the Profit percent\n\n```\npercent_change(\'AAPL\', \'2017-01-01\', \'2017-01-10\')\n```\n\n### To Visualize the profit percentage change trend of a stock against market benchmark\n\n```\nfig = profit_viz(\'AAPL\', \'2015-01-01\', \'2021-12-31\', \'SPY\')\nfig.show()\n```\n![**Percent Change**](https://github.com/UBC-MDS/pystockwatch/blob/main/docs/percent_change_example.png?raw=true)\n\n### To check daily trading volume change of a stock\n\n```\nvolume_change(\'AAPL\', \'2021-01-01\', \'2022-01-01\')\n```\n### To Visualize the volume change trend of a stock \n\n```\nvol = volume_viz(\'AAPL\', \'2021-01-01\', \'2022-01-01\')\nvol.show()\n```\n ![**Volume Change**](https://github.com/UBC-MDS/pystockwatch/blob/main/docs/volume_plot_example.png?raw=true)\n\n## Documentation\n\nThe documentation of this package is hosted on Read the Docs: [here](https://pystockwatch.readthedocs.io/)\n\n## Contributors\n\n* Affrin Sultana\n* Helin Wang\n* Pavel Levchenko\n* Shi Yan Wang\n\n## Contributing\n\nAre you interested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.\n\n## Dependencies\nBefore the installation of this package please install the following packages:\n\n* python = "^3.9"\n* pandas = "^1.3.5"\n* altair = "^4.2.0"\n* altair_viewer = "^0.4.0"\n* pandas-datareader = "^0.10.0"\n\n## License\n\n`pystockwatch` was created by Affrin Sultana, Helin Wang, Pavel Levchenko, Shi Yan Wang.It is licensed under the terms of the MIT license. \n\n## Credits\n\n`pystockwatch` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).\n',
    'author': 'Affrin Sultana, Helin Wang, Pavel Levchenko, Shi Yan Wang',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/UBC-MDS/pystockwatch',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
