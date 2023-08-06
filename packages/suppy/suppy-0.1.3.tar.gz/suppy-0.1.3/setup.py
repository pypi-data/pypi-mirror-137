# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['suppy',
 'suppy.strategy',
 'suppy.strategy.control',
 'suppy.strategy.release',
 'suppy.utils']

package_data = \
{'': ['*']}

install_requires = \
['tqdm>=4.62.3,<5.0.0', 'typeguard>=2.13.3,<3.0.0']

setup_kwargs = {
    'name': 'suppy',
    'version': '0.1.3',
    'description': '',
    'long_description': '# Suppy\n\n[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=chain-stock_suppy&metric=coverage)](https://sonarcloud.io/summary/new_code?id=chain-stock_suppy)\n[![Test](https://github.com/chain-stock/suppy/actions/workflows/tox.yml/badge.svg)](https://github.com/chain-stock/suppy/actions/workflows/tox.yml)\n[![PyPI version](https://badge.fury.io/py/suppy.svg)](https://badge.fury.io/py/suppy)\n\nSuppy allows simulating multi-item, multi-echelon (MIME) supply-chain systems\nwith support for user-defined inventory control and release policies.\n\n## Contributing\nA pre-commit config is included in this repo.\nThis will, among other things, run black and isort on your code changes\n\nTo enable the pre-commit hook, run `poetry run pre-commit install`\n',
    'author': 'Allex Veldman',
    'author_email': 'a.veldman@chain-stock.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/chain-stock/suppy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
