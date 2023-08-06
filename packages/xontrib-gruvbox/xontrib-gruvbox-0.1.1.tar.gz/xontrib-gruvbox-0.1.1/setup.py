# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['xontrib']

package_data = \
{'': ['*']}

install_requires = \
['xonsh']

setup_kwargs = {
    'name': 'xontrib-gruvbox',
    'version': '0.1.1',
    'description': 'A Gruvbox theme for xonsh.',
    'long_description': 'xontrib-gruvbox\n===============\n\n|pypi-badge|\n\n`Gruvbox <https://github.com/morhetz/gruvbox>`__ theme for xonsh.\n\nBased on\n`xontrib-dracula <https://github.com/agoose77/xontrib-dracula>`__ by\nAngus Hollands.\n\n.. |pypi-badge| image:: https://img.shields.io/pypi/v/xontrib-gruvbox\n   :target: https://pypi.org/project/xontrib-gruvbox\n',
    'author': 'Ryan Delaney',
    'author_email': 'ryan.patrick.delaney@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
