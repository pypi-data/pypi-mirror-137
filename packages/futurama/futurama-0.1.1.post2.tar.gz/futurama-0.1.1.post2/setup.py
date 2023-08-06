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
    'version': '0.1.1.post2',
    'description': 'Random Futurama Quotes',
    'long_description': '# futurama\n\nRandom Futurama Quotes\n\n[![Build Status](https://drone.decapod.one/api/badges/brethil/futurama/status.svg?ref=refs/heads/main)](https://drone.decapod.one/brethil/futurama)\n\n## Install\n\n```bash\npip install futurama\n```\n\n### Usage\n\nVia command-line:\n\n```\nfuturama\n```\n\nas a python module:\n\n```bash\npython -m futurama\n```\n',
    'author': 'brethil',
    'author_email': 'bretello@distruzione.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://git.decapod.one/brethil/futurama',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
