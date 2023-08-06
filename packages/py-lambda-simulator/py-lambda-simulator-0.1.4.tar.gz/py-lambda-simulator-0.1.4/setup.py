# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['py_lambda_simulator']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.1,<4.0.0',
 'asyncer>=0.0.1,<0.0.2',
 'boto3>=1.20.46,<2.0.0',
 'moto>=3.0.2,<4.0.0',
 'typing-extensions>=4.0.1,<5.0.0']

setup_kwargs = {
    'name': 'py-lambda-simulator',
    'version': '0.1.4',
    'description': '',
    'long_description': None,
    'author': 'Johan Bothin',
    'author_email': 'johan.bothin@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/hemma/py-lambda-simulator',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
