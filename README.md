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
from python_json_config.validators import is_unreserved_port, is_ipv4_address, is_timedelta
from python_json_config.transformers import to_timedelta
from datetime import datetime, timedelta

# create config parser
builder = ConfigBuilder()

# assert that port contains an int value
builder.validate_field_type('server.ip', str)
builder.validate_field_type('server.port', int)
builder.validate_field_type('jwt.access_token_expires', str)

# assert that the port is not a reserved port 
builder.validate_field_value('server.ip', is_ipv4_address)
builder.validate_field_value('server.port', is_unreserved_port)
builder.validate_field_value('jwt.access_token_expires', is_timedelta)

# return custom error messages in your lambdas
builder.validate_field_value('server.ip', lambda ip: (ip != '0.0.0.0', 'IP is unroutable.'))

# chain validation functions
builder.validate_field_value('server.ip', [lambda ip: ip != 'localhost', lambda ip: ip != '127.0.0.1'])

# parse a timedelta (e.g., Jun 1 2005) into a datetime object
builder.transform_field_value('important_date', lambda date: datetime.strptime(date, '%b %d %Y'))
builder.transform_field_value('jwt.access_token_expires', to_timedelta)

# parse config
config = builder.parse_config('path/to/config.json')

# access config values
port = config.server.port
assert port > 1023

ip = config.server.ip
assert ip not in ['0.0.0.0', 'localhost', '127.0.0.1']

important_date = config.important_date
assert isinstance(important_date, datetime)

jwt_access_token_expires = config.jwt.access_token_expires
assert isinstance(jwt_access_token_expires, timedelta)
```
