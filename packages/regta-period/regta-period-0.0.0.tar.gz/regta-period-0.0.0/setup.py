# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['regta_period']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'regta-period',
    'version': '0.0.0',
    'description': 'Time-independent periods python package',
    'long_description': '# periods\nTime-independent periods python package\n',
    'author': 'Vladimir Alinsky',
    'author_email': 'Vladimir@Alinsky.tech',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/SKY-ALIN/periods',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
