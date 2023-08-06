# YAMSL
![License](https://img.shields.io/github/license/gwrd-ch/yamsl)

Yet Another Meteo Swiss Library

## General Info
This python library provides an easy way to get forecasts from MeteoSwiss.

## Installation
Install with pip:
```
$ pip install yamsl
```

## Usage

```
from yamsl import MeteoSwiss


meteo = MeteoSwiss() # instanciate MeteoSwiss
await meteo.setup(8001) # setup with zip-code
forecast = await meteo.updateForecast() # update forecast (also returns forecast)
```

## Licence


## Disclaimer
The code is provided as is. This is an unofficial client.

## Thanks
* This repo helped a lot: https://github.com/caco3/MeteoSwiss-Forecast

## Development

After cloning repo:
```
// Create the virtual environment
$ python3 -m venv venv
$ python -m venv venv

// Activate the virtual environment (Linux/macOS)
$ source venv/bin/activate

// Install requirements
$ pip install -r requirements.txt
```

Before checking in again:
```
// Freeze requirements
$ pip freeze > requirements.txt
```

## Deploy

Compile and test
```
python setup.py sdist bdist_wheel
twine check dist/*
twine upload --repository-url https://test.pypi.org/legacy/ dist/*
twine upload dist/*
```