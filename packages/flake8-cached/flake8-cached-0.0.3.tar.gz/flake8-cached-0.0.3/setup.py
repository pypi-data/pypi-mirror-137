# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flake8_cached']

package_data = \
{'': ['*']}

install_requires = \
['flake8>=3.9.0']

entry_points = \
{'console_scripts': ['flake8-cached = flake8_cached.cli:main']}

setup_kwargs = {
    'name': 'flake8-cached',
    'version': '0.0.3',
    'description': "A wrapper around flake8's cli that uses cache at file level",
    'long_description': "# Overview\n\nA wrapper around flake8's cli that caches results between runs at file level.\n\nThis project was generated with [cookiecutter](https://github.com/audreyr/cookiecutter) using [jacebrowning/template-python](https://github.com/jacebrowning/template-python).\n\n[![Unix Build Status](https://img.shields.io/travis/com/jnoortheen/flake8-cached.svg?label=unix)](https://travis-ci.com/jnoortheen/flake8-cached)\n[![Windows Build Status](https://img.shields.io/appveyor/ci/jnoortheen/flake8-cached.svg?label=windows)](https://ci.appveyor.com/project/jnoortheen/flake8-cached)\n[![Coverage Status](https://img.shields.io/coveralls/jnoortheen/flake8-cached.svg)](https://coveralls.io/r/jnoortheen/flake8-cached)\n[![Scrutinizer Code Quality](https://img.shields.io/scrutinizer/g/jnoortheen/flake8-cached.svg)](https://scrutinizer-ci.com/g/jnoortheen/flake8-cached)\n[![PyPI Version](https://img.shields.io/pypi/v/flake8-cached.svg)](https://pypi.org/project/flake8-cached)\n[![PyPI License](https://img.shields.io/pypi/l/flake8-cached.svg)](https://pypi.org/project/flake8-cached)\n\n# Setup\n\n## Requirements\n\n* Python 3.6+\n\n## Installation\n\nInstall it directly into an activated virtual environment:\n\n```text\n$ pip install flake8-cached\n```\n\nor add it to your [Poetry](https://poetry.eustace.io/) project:\n\n```text\n$ poetry add flake8-cached\n```\n\n# Usage\n\nAfter installation, the package can imported:\n\n```shell\n# it accepts all arguments as flake8\n$ flake8-cached .\n```\n\n# Note\n\nIt creates cache files under `.cache/flake8` under the project directory. \nIt is not cleaned up even if there is some config or python binary changes. \nPlease remove the folder and re-run if you get stale results.\nIt is a simple cache implementation intended to be used during development.\n",
    'author': 'Noortheen Raja ',
    'author_email': 'jnoortheen@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://pypi.org/project/flake8-cached',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
