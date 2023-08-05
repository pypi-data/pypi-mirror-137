# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pytest_container']

package_data = \
{'': ['*']}

install_requires = \
['filelock>=3.4,<4.0', 'pytest-testinfra>=6.4.0', 'pytest>=3.10']

extras_require = \
{':python_version < "3.7"': ['dataclasses>=0.8']}

entry_points = \
{'pytest11': ['pytest11.container = pytest_container.plugin']}

setup_kwargs = {
    'name': 'pytest-container',
    'version': '0.0.2',
    'description': 'Pytest fixtures for writing container based tests',
    'long_description': None,
    'author': 'Dan Čermák',
    'author_email': 'dcermak@suse.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2,<4.0',
}


setup(**setup_kwargs)
