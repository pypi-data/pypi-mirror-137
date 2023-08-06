# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['poisonlib', 'poisonlib.partitioners', 'poisonlib.poisoners']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.22.2,<2.0.0', 'scipy>=1.7.3,<2.0.0', 'sklearn>=0.0,<0.1']

setup_kwargs = {
    'name': 'poisonlib',
    'version': '0.1.0',
    'description': 'A library for algorithmic poisoning of machine learning datasets',
    'long_description': None,
    'author': 'srthiru',
    'author_email': 'srthiruvenkadam@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
