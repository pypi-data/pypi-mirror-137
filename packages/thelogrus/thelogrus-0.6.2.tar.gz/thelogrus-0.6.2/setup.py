# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['thelogrus']

package_data = \
{'': ['*']}

install_requires = \
['dateutils>=0.6.12,<0.7.0', 'pyaml>=21.10.1,<22.0.0']

entry_points = \
{'console_scripts': ['human-time = thelogrus.time:human_time_converter']}

setup_kwargs = {
    'name': 'thelogrus',
    'version': '0.6.2',
    'description': 'The Logrus is a collection of random utility functions',
    'long_description': None,
    'author': 'Joe Block',
    'author_email': 'jpb@unixorn.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/unixorn/thelogrus',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
