[![Build Status](https://travis-ci.com/janehmueller/python-config.svg?token=tGKCTy4zTZfGNfjpEgEX&branch=master)](https://travis-ci.com/janehmueller/python-config)
![License](https://img.shields.io/pypi/l/python-json-config.svg)
[![Version](https://img.shields.io/pypi/v/python-json-config.svg)](https://pypi.python.org/pypi/python-json-config/)

# Overview
This library allows to load json configs and access the values like members (i.e., `config.server.port`
instead of `config['server']['port']`), validate the data types of fields and transform the values of fields.

# Installing
```
pip install python-json-config
```
# Usage
```
from python_json_config import ConfigBuilder
from datetime import datetime

# create config parser
builder = ConfigBuilder()

# assert that port contains an int value
builder.validate_field_type('server.port', int)

# assert that the port is not a reserved port 
builder.validate_field_value('server.port', lambda port: port > 1024)

# parse a date string (e.g., Jun 1 2005) into a datetime object
builder.transform_field_value('important_date', lambda date: datetime.strptime(date, '%b %d %Y'))

# parse config
config = builder.parse_config('path/to/config.json')

# access config values
port = config.server.port
assert isinstance(port, int)
important_date = config.important_date
assert isinstance(important_date, datetime)
```
