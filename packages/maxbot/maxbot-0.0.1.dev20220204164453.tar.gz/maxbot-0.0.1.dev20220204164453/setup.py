# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['maxbot', 'maxbot.commands']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'requests>=2.27.1,<3.0.0',
 'typer[all]>=0.4.0,<0.5.0',
 'wasabi>=0.9.0,<0.10.0']

entry_points = \
{'console_scripts': ['maxbot = maxbot:app']}

setup_kwargs = {
    'name': 'maxbot',
    'version': '0.0.1.dev20220204164453',
    'description': '',
    'long_description': None,
    'author': 'Stanislav Arsentyev',
    'author_email': 'arstas@gmail.com',
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
