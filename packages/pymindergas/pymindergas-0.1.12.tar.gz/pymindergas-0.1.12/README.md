# pymindergas

A module to post meter readings to [MinderGas.nl][mindergas].

## Installation

```shell
$ pip3 install pymindergas
```

## Usage

In order to be able to post readings, you first need to obtain an [API][api] token.

The `postReading()` method requires an authentication token (String) and the meter reading (Float). The reading date can be any valid date (String), but is optional.

Parameter | Required | Description
--- | --- | ---
token | yes | String
reading | yes | Float
date | no | Any date string that can be [parsed][parse]. If not passed, uses today.

Code sample:

```python
from datetime import date
from datetime import timedelta
from pymindergas import Mindergas

token = "supersecretstring"
reading = 1234.567
yesterday = date.today() - timedelta(days = 1)

# Post reading as yesterday's
success = Mindergas().postReading(token, reading, yesterday.strftime('%y-%m-%d'))
print(success)

# Post reading as today's
success = Mindergas().postReading(token, reading)
print(success)
```

## Disclaimer

This is an open source project and does not have any affiliation with [MinderGas.nl][mindergas].

All product names, trademarks and registered trademarks in this repository are property of their respective owners. All images in this repository are used by the project for identification purposes only.

[mindergas]: https://www.mindergas.nl/
[api]: https://www.mindergas.nl/member/api
[parse]: https://dateutil.readthedocs.io/en/stable/parser.html#dateutil.parser.parse
