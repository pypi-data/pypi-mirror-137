# Stock Market MBA API

A simple library for accessing data from [stockmarketmba.com](https://stockmarketmba.com).

API queries currently return a JSON object, however future development will allow further options such as a Pandas DataFrame and CSV.

## Current Endpoints

* **Symbol lookup** - *returns stock identifiers*
* **Stocks on Exchange** - *returns list of stocks on a particular exchange*
* **Global Exchange Symbols** - *returns a list of exchange symbols for use with other endpoints*
* **Pending SPACS** - *returns a list of pending SPACs*

## Install

```shell
    pip install stockmarketmba
```

## Future Development

- [ ] Add more endpoints
- [ ] Add more output options (pandas, csv, etc.)