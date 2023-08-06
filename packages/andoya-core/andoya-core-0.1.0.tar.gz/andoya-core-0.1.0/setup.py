# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['andoya', 'andoya.core', 'andoya.core.stubs']

package_data = \
{'': ['*']}

install_requires = \
['tomlkit>=0.8.0,<0.9.0']

setup_kwargs = {
    'name': 'andoya-core',
    'version': '0.1.0',
    'description': 'The Andoya Core package.',
    'long_description': None,
    'author': 'Ian Rodrigues',
    'author_email': 'ianrdgs@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
