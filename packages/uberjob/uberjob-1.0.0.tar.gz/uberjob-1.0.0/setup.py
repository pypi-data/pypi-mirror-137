# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['uberjob',
 'uberjob._execution',
 'uberjob._testing',
 'uberjob._transformations',
 'uberjob._util',
 'uberjob.progress',
 'uberjob.stores']

package_data = \
{'': ['*']}

install_requires = \
['networkx>=2.5,<3.0', 'nxv>=0.1.3,<0.2.0']

setup_kwargs = {
    'name': 'uberjob',
    'version': '1.0.0',
    'description': 'uberjob is a Python package for building and running call graphs.',
    'long_description': '<img src="https://github.com/twosigma/uberjob/raw/main/docs/_static/logo/logo-128.png" align="right">\n\n# uberjob\n\n[![PyPI Status](https://img.shields.io/pypi/v/uberjob.svg)](https://pypi.python.org/pypi/uberjob)\n[![Tests](https://github.com/twosigma/uberjob/workflows/Tests/badge.svg)](https://github.com/twosigma/uberjob/actions)\n[![Documentation Status](https://readthedocs.org/projects/uberjob/badge/?version=latest)](https://uberjob.readthedocs.io/en/latest/?badge=latest)\n[![Codecov](https://codecov.io/gh/twosigma/uberjob/branch/main/graph/badge.svg)](https://codecov.io/gh/twosigma/uberjob)\n\n\nuberjob is a Python package for building and running call graphs.\n\n# Documentation\n\nhttps://uberjob.readthedocs.io/\n\n# Installation\n\n    pip install uberjob\n\n# Development\n\nThis repository uses\n[Poetry](https://python-poetry.org/) and\n[Nox](https://nox.thea.codes/en/stable/)\nto manage the development environment and builds.\n\nTo list all Nox sessions:\n\n    python -m nox --list-sessions\n\nTo run the black code formatter:\n\n    python -m nox -rs black\n\nTo lint using flake8:\n\n    python -m nox -rs lint\n\nTo run the test suite:\n\n    python -m nox -rs tests\n\nTo build the documentation:\n\n    python -m nox -rs docs\n',
    'author': 'Timothy Shields',
    'author_email': 'Timothy.Shields@twosigma.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/twosigma/uberjob',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
