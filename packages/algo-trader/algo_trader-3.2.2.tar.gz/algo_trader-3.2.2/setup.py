# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['algo_trader',
 'algo_trader.clients',
 'algo_trader.clients.binance',
 'algo_trader.clients.bitmex',
 'algo_trader.settings',
 'algo_trader.strategies']

package_data = \
{'': ['*']}

install_requires = \
['binance>=0.3,<0.4', 'bitmex>=0.2.2,<0.3.0', 'bravado>=11.0.3,<12.0.0']

entry_points = \
{'console_scripts': ['algotrader = algo_trader.startbot:app']}

setup_kwargs = {
    'name': 'algo-trader',
    'version': '3.2.2',
    'description': '"Trade execution engine to process API data and transmit orders to Bitmex and other brokers."',
    'long_description': None,
    'author': 'Niclas Hummel',
    'author_email': 'info@algoinvest.online',
    'maintainer': 'Niclas Hummel',
    'maintainer_email': 'info@algoinvest.online',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<3.10',
}


setup(**setup_kwargs)
