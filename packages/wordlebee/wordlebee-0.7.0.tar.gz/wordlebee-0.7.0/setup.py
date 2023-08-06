# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wordlebee']

package_data = \
{'': ['*'], 'wordlebee': ['data/*']}

install_requires = \
['numpy>=1.22.1,<2.0.0', 'rich>=11.0.0,<12.0.0']

entry_points = \
{'console_scripts': ['wordlebee = wordlebee.__main__:cli'],
 'pipx.run': ['wordlebee = wordlebee.__main__:cli']}

setup_kwargs = {
    'name': 'wordlebee',
    'version': '0.7.0',
    'description': 'wordle word guessing helper bee',
    'long_description': '<div align="center">\n\n<h1>\n    <img width="500" align="center" src="assets/wordlebee-logo.svg">\n</h1>\n\n[![PyPi Version](https://img.shields.io/pypi/v/wordlebee.svg?style=flat-square)](https://pypi.org/project/wordlebee/)\n[![PyPi Python versions](https://img.shields.io/pypi/pyversions/wordlebee.svg?style=flat-square)](https://pypi.org/project/wordlebee/)\n[![License](https://img.shields.io/badge/license-MIT-blue?style=flat-square)](#license)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square)](#black)\n[![Downloads](https://pepy.tech/badge/wordlebee?style=flat-square)](https://pepy.tech/project/wordlebee)\n\n***A cli wordle word guessing helper bee to solve the wordle puzzle of the day.***\n\n</div>\n\n## Usage\n\n```\npython -m wordlebee\n```\n\n## Installation\n\nInstall `wordlebee` in isolated environment:\n\n```\npipx install wordlebee\n```\n\nInstall `wordlebee`:\n\n```\npip install wordlebee\n```\n\n## Development\n\nInstall conda enviroment:\n\n```\nconda env create -f environment.yml\n```\n\nInstall using `poetry`:\n\n```\npoetry install\n```\n',
    'author': 'Mrlento234',
    'author_email': 'lento.manickathan@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
