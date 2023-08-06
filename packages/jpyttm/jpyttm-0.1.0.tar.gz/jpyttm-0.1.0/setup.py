# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jpyttm']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.10.0,<5.0.0',
 'lxml>=4.7.1,<5.0.0',
 'pytz>=2021.3,<2022.0',
 'requests>=2.27.1,<3.0.0']

setup_kwargs = {
    'name': 'jpyttm',
    'version': '0.1.0',
    'description': 'Historical JPY TTM rates',
    'long_description': 'JPY TTM Rates\n-------------\n\nHistorical JPY TTM rates, basically for tax purposes.\n\nInstall\n-------\n\nInstall from PyPI:\n\n```pip install jpyttm```\n\nUsage\n-----\n\n```python\nfrom jpyttm import USD, get_historical_ttm\n\nttm = get_historical_ttm(USD)\nfor quote in ttm:\n    print(quote[0], quote[1])\n```\n\nTo specify a range, call `get_historical_ttm` with optional parameters `timestamp_from` and/or `timestamp_to`\n',
    'author': 'Alex',
    'author_email': 'globophobe@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/globophobe/jpyttm',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
