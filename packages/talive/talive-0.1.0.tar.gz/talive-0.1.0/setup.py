# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['talive']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'talive',
    'version': '0.1.0',
    'description': 'Technical Analysis for LIVE trading',
    'long_description': None,
    'author': 'Zou Yilin',
    'author_email': 'zouyilin2@yandex.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
