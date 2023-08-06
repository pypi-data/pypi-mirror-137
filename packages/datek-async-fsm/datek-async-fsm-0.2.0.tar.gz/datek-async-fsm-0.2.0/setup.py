# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['datek_async_fsm']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'datek-async-fsm',
    'version': '0.2.0',
    'description': 'Asynchronous Finite State Machine',
    'long_description': '[![codecov](https://codecov.io/gh/DAtek/datek-async-fsm/branch/master/graph/badge.svg?token=4OHS9GMM5D)](https://codecov.io/gh/DAtek/datek-async-fsm)\n<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>\n<a href="https://github.com/psf/black/blob/main/LICENSE"><img alt="License: MIT" src="https://black.readthedocs.io/en/stable/_static/license.svg"></a>\n\n# Asynchronous Finite State Machine\nFor an example see [`tests/example.py`](https://gitlab.com/DAtek/datek-async-fsm/-/blob/master/tests/example.py)',
    'author': 'Attila Dudas',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/DAtek/datek-async-fsm/',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
