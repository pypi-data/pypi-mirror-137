JPY TTM Rates
-------------

Historical JPY TTM rates, basically for tax purposes.

Install
-------

Install from PyPI:

```pip install jpyttm```

Usage
-----

```python
from jpyttm import USD, get_historical_ttm

ttm = get_historical_ttm(USD)
for quote in ttm:
    print(quote[0], quote[1])
```

To specify a range, call `get_historical_ttm` with optional parameters `timestamp_from` and/or `timestamp_to`
