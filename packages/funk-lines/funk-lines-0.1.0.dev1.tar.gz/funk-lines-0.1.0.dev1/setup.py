# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['funk_lines',
 'funk_lines.core',
 'funk_lines.core.analysers',
 'funk_lines.core.ast_processors']

package_data = \
{'': ['*']}

install_requires = \
['rich>=11.1.0,<12.0.0', 'typer>=0.4.0,<0.5.0']

entry_points = \
{'console_scripts': ['funk-lines = funk_lines.__main__:app']}

setup_kwargs = {
    'name': 'funk-lines',
    'version': '0.1.0.dev1',
    'description': 'Funk Lines',
    'long_description': '# Funk Lines\n\n[//]: # "[![PyPI](https://img.shields.io/pypi/v/funk-lines.svg)](https://pypi.org/project/funk-lines)"\n[//]: # "[![Python Version](https://img.shields.io/pypi/pyversions/funk-lines)](https://pypi.org/project/funk-lines)"\n[//]: # "[![License](https://img.shields.io/pypi/l/funk-lines)](https://opensource.org/licenses/MIT)"\n\n[![Build](https://github.com/federicober/funk-lines/actions/workflows/build.yml/badge.svg)](https://github.com/federicober/funk-lines/actions/workflows/build.yml)\n[![codecov](https://codecov.io/gh/federicober/funk-lines/branch/main/graph/badge.svg?token=3I0fVVBTOG)](https://codecov.io/gh/federicober/funk-lines)\n\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)\n[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\n---\n\nCalculate the average number of code lines per function or class definition.\n\n## Installation\n\nYou can install _Funk Lines_ via `pip` from [PyPI](https://pypi.org/):\n\n```shell\n$ pip install funk-lines\n```\n\n## Usage\n\nUse _Funk Lines_ via the console:\n\n```shell\n$ funk-lines /path/to/script.py\n```\n\n## License\n\nDistributed under the terms of the MIT\\_ license,\n_Funk Lines_ is free and open source software.\n',
    'author': 'Federico Oberndorfer',
    'author_email': 'federico.ober@hotmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/federicober/funk-lines',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10.2,<4.0.0',
}


setup(**setup_kwargs)
