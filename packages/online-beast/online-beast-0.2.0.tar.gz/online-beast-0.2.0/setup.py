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
    'version': '0.2.0',
    'description': '',
    'long_description': '# online-BEAST\n[![PyPi](https://img.shields.io/pypi/v/online-beast.svg)](https://pypi.org/project/online-beast/)\n[![tests](https://github.com/Wytamma/online-beast/actions/workflows/test.yml/badge.svg)](https://github.com/Wytamma/online-beast/actions/workflows/test.yml)\n[![cov](https://codecov.io/gh/Wytamma/online-beast/branch/master/graph/badge.svg)](https://codecov.io/gh/Wytamma/online-beast)\n',
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
