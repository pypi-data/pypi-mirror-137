# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mongodb_connector']

package_data = \
{'': ['*']}

install_requires = \
['lark-parser>=0.12.0,<0.13.0', 'pymongo>4.0.1']

setup_kwargs = {
    'name': 'mongodb-connector',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>3.7',
}


setup(**setup_kwargs)
