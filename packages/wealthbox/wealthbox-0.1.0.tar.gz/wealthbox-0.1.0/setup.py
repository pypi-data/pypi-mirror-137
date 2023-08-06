# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wealthbox']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.27.1,<3.0.0']

setup_kwargs = {
    'name': 'wealthbox',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'spencerogden-dsam',
    'author_email': '67068943+spencerogden-dsam@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
