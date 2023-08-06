# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aussiebb', 'aussiebb.asyncio']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.1,<4.0.0', 'requests>=2.27.1,<3.0.0']

setup_kwargs = {
    'name': 'pyaussiebb',
    'version': '0.0.11',
    'description': 'Aussie Broadband API module',
    'long_description': None,
    'author': 'James Hodgkinson',
    'author_email': 'james@terminaloutcomes.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/yaleman/aussiebb',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
