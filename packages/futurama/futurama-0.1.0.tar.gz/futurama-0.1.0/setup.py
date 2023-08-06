# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['futurama']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['futurama = futurama.__main__:main']}

setup_kwargs = {
    'name': 'futurama',
    'version': '0.1.0',
    'description': 'Random Futurama Quotes',
    'long_description': None,
    'author': 'brethil',
    'author_email': 'bretello@distruzione.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
