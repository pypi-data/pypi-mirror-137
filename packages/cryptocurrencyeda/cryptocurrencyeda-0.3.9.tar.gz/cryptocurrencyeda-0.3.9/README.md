# cryptocurrencyeda

[![ci-cd](https://github.com/UBC-MDS/cryptocurrencyeda/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/UBC-MDS/cryptocurrencyeda/actions/wokflows/ci-cd.yml)

This is a Python package to analyze historical cryptocurrency prices and performance through simple exploratory data analysis including calculations and plotting. Data is sourced from the KuCoin API. There are four functions that are included in this python package which are described in more detail below. Cryptocurrency investors and enthusiasts can use this package to analyze cryptocurrencies of interest.


There are existing Python libraries to access information of cryptocurrency such as [cryptocompare](https://github.com/lagerfeuer/cryptocompare) and [cryptofeed](https://github.com/bmoscon/cryptofeed). There are also existing Python libraries to visualize financial data such as [mplfinance](https://github.com/matplotlib/mplfinance).
However, there is no integrated Python library for accessing, analyzing, and visualizing cryptocurrency data altogether. Therefore, we want to build a simple tool that can facilitate simple cryptocurrency data analysis all at once.

## Function List

The package contains the following four functions:

- `retrieve_data`: downloads historical data from a cryptocurrency exchange using an an http request from a cryptocurrency exchange.

- `plot_price`: generates and visualizes a plot of the price of the cryptocurrenty inputted over a period of time.

- `daily_growth_rate`: performs calculation of daily growth rate of the cryptocurrenty inputted over a period of time.

- `avg_daily_return`: performs calculation of the average daily return of the inputted cryptocurrency price.
## Installation and Usage

In order to use the package, please follow these steps: 
#### Create a new conda environment:

```
conda create --name cryptocurrencyeda python=3.9 -y
```
#### Activate the environment:
```
conda activate cryptocurrencyeda
```
#### Install the package:
```
pip install cryptocurrencyeda
or 
pip install git+https://github.com/UBC-MDS/cryptocurrencyeda
```
#### Open Python:
```
Python
```
#### Import all functions:
```
>>> from cryptocurrencyeda.retrieve_data import retrieve_data
>>> from cryptocurrencyeda.plot_price import plot_price
>>> from cryptocurrencyeda.avg_daily_return import avg_daily_return
>>> from cryptocurrencyeda.daily_growth_rate import daily_growth_rate
```
#### Use the functions: 
```
>>> retrieve_data(symbol="BTC-USDT",
                  time_period="1day",
                  start_date="2018-01-01",
                  end_date="2022-01-10",
                 )

>>> plot_price(price_df)

>>> daily_growth_rate(price_df, "Close")

>>> avg_daily_return(price_df["Close"])
```

## Documentation

The documentation is hosted on ReadTheDocs [here](https://cryptocurrencyeda.readthedocs.io/en/latest/)
## Contributors

We welcome and recognize all contributions. You can see a list of current contributors in the [`contributors tab`](https://github.com/UBC-MDS/CryptocurrencyEDA/graphs/contributors). If you are interested in contributing to this project, please check out our CONDUCT.md

- Berkay Bulut
- Cici Du
- Alex Yinan Guo
- Nobby Nguyen

## License

`cryptocurrencyeda` was created by MDS Students from Group-11 for course 524. It is licensed under the terms of the MIT license.

## Credits

`cryptocurrencyeda` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).
