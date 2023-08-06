# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['countdown']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.1,<9.0.0']

entry_points = \
{'console_scripts': ['countdown = countdown.__main__:main']}

setup_kwargs = {
    'name': 'countdown-cli',
    'version': '1.0.1',
    'description': 'Terminal program to display countdown timer',
    'long_description': "countdown-cli\n=============\n\n|PyPI| |Status| |Python Version| |License|\n\n|Read the Docs| |Tests| |Codecov|\n\n|pre-commit| |Black|\n\n.. |PyPI| image:: https://img.shields.io/pypi/v/countdown-cli.svg\n   :target: https://pypi.org/project/countdown-cli/\n   :alt: PyPI\n.. |Status| image:: https://img.shields.io/pypi/status/countdown-cli.svg\n   :target: https://pypi.org/project/countdown-cli/\n   :alt: Status\n.. |Python Version| image:: https://img.shields.io/pypi/pyversions/countdown-cli\n   :target: https://pypi.org/project/countdown-cli\n   :alt: Python Version\n.. |License| image:: https://img.shields.io/pypi/l/countdown-cli\n   :target: https://opensource.org/licenses/MIT\n   :alt: License\n.. |Read the Docs| image:: https://img.shields.io/readthedocs/countdown-cli/latest.svg?label=Read%20the%20Docs\n   :target: https://countdown-cli.readthedocs.io/\n   :alt: Read the documentation at https://countdown-cli.readthedocs.io/\n.. |Tests| image:: https://github.com/treyhunner/countdown-cli/workflows/Tests/badge.svg\n   :target: https://github.com/treyhunner/countdown-cli/actions?workflow=Tests\n   :alt: Tests\n.. |Codecov| image:: https://codecov.io/gh/treyhunner/countdown-cli/branch/main/graph/badge.svg\n   :target: https://codecov.io/gh/treyhunner/countdown-cli\n   :alt: Codecov\n.. |pre-commit| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white\n   :target: https://github.com/pre-commit/pre-commit\n   :alt: pre-commit\n.. |Black| image:: https://img.shields.io/badge/code%20style-black-000000.svg\n   :target: https://github.com/psf/black\n   :alt: Black\n\nThis project is based on a `Python Morsels`_ exercise for a command-line countdown timer.\nIf you're working on that exercise right now, please **don't look at the source code** for this. 😉\n\n|Logo|\n\n.. |Logo| image:: https://countdown-cli.readthedocs.io/en/latest/_images/python-morsels-logo.png\n   :target: https://www.pythonmorsels.com\n   :width: 400\n   :alt: an adorable snake taking a bite out of a cookie with the words Python Morsels next to it (Python Morsels logo)\n\n\nFeatures\n--------\n\n* Full-screen countdown timer, centered in the terminal window\n* Command-line interface for Linux/Mac/Windows\n\n|32:53|\n\n|14:57|\n\n.. |32:53| image:: https://countdown-cli.readthedocs.io/en/latest/_images/3253.png\n   :width: 500\n   :alt: 32:53 shown in large letters in center of an xterm window (black background with white text)\n\n.. |14:57| image:: https://countdown-cli.readthedocs.io/en/latest/_images/1457.png\n   :width: 500\n   :alt: 14:57 shown in large letters in center of terminal window (light background with darker text)\n\n\nRequirements\n------------\n\n* Python 3.7+\n\n\nInstallation\n------------\n\nYou can install *countdown-cli* via pip_ from PyPI_:\n\n.. code:: console\n\n   $ python3 -m pip install countdown-cli\n\n\nUsage\n-----\n\nPlease see the `Command-line Reference <Usage_>`_ for details.\n\n\nContributing\n------------\n\nContributions are very welcome.\nTo learn more, see the `Contributor Guide`_.\n\n\nLicense\n-------\n\nDistributed under the terms of the `MIT license`_,\n*countdown-cli* is free and open source software.\n\n\nIssues\n------\n\nIf you encounter any problems,\nplease `file an issue`_ along with a detailed description.\n\n\nCredits\n-------\n\nThis project was generated from `@cjolowicz`_'s `Hypermodern Python Cookiecutter`_ template.\n\n.. _Python Morsels: https://www.pythonmorsels.com\n.. _@cjolowicz: https://github.com/cjolowicz\n.. _Cookiecutter: https://github.com/audreyr/cookiecutter\n.. _MIT license: https://opensource.org/licenses/MIT\n.. _PyPI: https://pypi.org/project/countdown-cli/\n.. _Hypermodern Python Cookiecutter: https://github.com/cjolowicz/cookiecutter-hypermodern-python\n.. _file an issue: https://github.com/treyhunner/countdown-cli/issues\n.. _pip: https://pip.pypa.io/\n.. github-only\n.. _Contributor Guide: CONTRIBUTING.rst\n.. _Usage: https://countdown-cli.readthedocs.io/en/latest/usage.html\n",
    'author': 'Trey Hunner',
    'author_email': 'trey@treyhunner.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/treyhunner/countdown-cli',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
