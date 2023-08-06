# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pipautocompile']

package_data = \
{'': ['*']}

install_requires = \
['click>=8,<9', 'python-on-whales>=0.36.0,<0.37.0']

entry_points = \
{'console_scripts': ['pip-autocompile = pipautocompile.main:cli']}

setup_kwargs = {
    'name': 'pip-autocompile',
    'version': '0.7.0',
    'description': 'Automate pip-compile for multiple environments.',
    'long_description': '# pip-autocompile\n\n[![lint](https://github.com/KSmanis/pip-autocompile/workflows/lint/badge.svg)](https://github.com/KSmanis/pip-autocompile/actions?workflow=lint)\n[![test](https://github.com/KSmanis/pip-autocompile/workflows/test/badge.svg)](https://github.com/KSmanis/pip-autocompile/actions?workflow=test)\n[![PyPI version](https://img.shields.io/pypi/v/pip-autocompile.svg)](https://pypi.org/project/pip-autocompile/)\n[![pre-commit enabled](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)\n[![Renovate enabled](https://img.shields.io/badge/renovate-enabled-brightgreen.svg)](https://renovatebot.com/)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)\n[![security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)\n[![Maintainability](https://api.codeclimate.com/v1/badges/87818991157d33ec5421/maintainability)](https://codeclimate.com/github/KSmanis/pip-autocompile/maintainability)\n[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-yellow.svg)](https://conventionalcommits.org)\n\nAutomate pip-compile for multiple environments.\n\n## Dependencies\n\n### Runtime\n\n- [pip-tools](https://github.com/jazzband/pip-tools): Compile requirements\n  locally\n- [Git](https://git-scm.com/) >= 2.13: Skip Git submodules when\n  `--no-git-recurse-submodules`\n',
    'author': 'Konstantinos Smanis',
    'author_email': 'konstantinos.smanis@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/KSmanis/pip-autocompile',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
