# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['stopwatch']

package_data = \
{'': ['*']}

install_requires = \
['colorama>=0.4.4,<0.5.0']

setup_kwargs = {
    'name': 'python-stopwatch2',
    'version': '0.1.0',
    'description': 'A simple stopwatch for Python',
    'long_description': '# Python-Stopwatch2\n',
    'author': 'Rafael',
    'author_email': 'contact.devrma@gmail.com',
    'maintainer': 'Rafael',
    'maintainer_email': 'contact.devrma@gmail.com',
    'url': 'https://github.com/devRMA/python-stopwatch2',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
