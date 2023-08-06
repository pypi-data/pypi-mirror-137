# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['envawareconfig']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0', 'python-dotenv>=0.19.2,<0.20.0']

setup_kwargs = {
    'name': 'envawareconfig',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'marcello',
    'author_email': 'marcello.frattini7@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
