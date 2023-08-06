# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['s3x', 's3x.utils']

package_data = \
{'': ['*']}

install_requires = \
['tqdm>=4.62.3,<5.0.0']

entry_points = \
{'console_scripts': ['s3x = s3x.main:cli']}

setup_kwargs = {
    'name': 's3x',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Dan Sikes',
    'author_email': 'dansikes7@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
