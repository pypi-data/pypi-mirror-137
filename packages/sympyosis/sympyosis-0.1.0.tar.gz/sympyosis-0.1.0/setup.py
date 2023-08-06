# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sympyosis', 'sympyosis.app', 'sympyosis.config', 'sympyosis.services']

package_data = \
{'': ['*']}

install_requires = \
['bevy>=1.0.1,<2.0.0', 'fastapi>=0.73.0,<0.74.0', 'psutil>=5.9.0,<6.0.0']

setup_kwargs = {
    'name': 'sympyosis',
    'version': '0.1.0',
    'description': 'Lightweight service orchistration & discovery.',
    'long_description': None,
    'author': 'Zech Zimmerman',
    'author_email': 'hi@zech.codes',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
