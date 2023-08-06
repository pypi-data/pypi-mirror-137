# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['online_beast']

package_data = \
{'': ['*']}

install_requires = \
['biopython>=1.79,<2.0', 'typer[all]']

entry_points = \
{'console_scripts': ['online-beast = online_beast.main:app']}

setup_kwargs = {
    'name': 'online-beast',
    'version': '0.1.0',
    'description': '',
    'long_description': '# online BEAST',
    'author': 'Wytamma Wirth',
    'author_email': 'wytamma.wirth@me.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2,<4.0',
}


setup(**setup_kwargs)
