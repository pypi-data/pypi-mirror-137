# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['load_stock_price_into_bigquery']

package_data = \
{'': ['*']}

install_requires = \
['google-cloud-bigquery>=2.32.0,<3.0.0',
 'numpy>=1.22.2,<2.0.0',
 'pandas-datareader>=0.10.0,<0.11.0',
 'pandas>=1.4.0,<2.0.0']

entry_points = \
{'console_scripts': ['load-stock-price-into-bigquery = '
                     'load_stock_price_into_bigquery.main:main']}

setup_kwargs = {
    'name': 'load-stock-price-into-bigquery',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'tyama711',
    'author_email': 'tyama711@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<3.11',
}


setup(**setup_kwargs)
