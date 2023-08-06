# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['snakebids',
 'snakebids.core',
 'snakebids.project_template.{{cookiecutter.app_name}}',
 'snakebids.project_template.{{cookiecutter.app_name}}.docs',
 'snakebids.project_template.{{cookiecutter.app_name}}.{{cookiecutter.app_name}}',
 'snakebids.resources',
 'snakebids.utils']

package_data = \
{'': ['*'],
 'snakebids': ['project_template/*'],
 'snakebids.project_template.{{cookiecutter.app_name}}': ['config/*',
                                                          'workflow/*'],
 'snakebids.project_template.{{cookiecutter.app_name}}.docs': ['getting_started/*',
                                                               'usage/*']}

install_requires = \
['PyYAML>=5.3.1,<6.0.0',
 'attrs>=21.2.0,<22.0.0',
 'boutiques>=0.5.25,<0.6.0',
 'colorama>=0.4.4,<0.5.0',
 'cookiecutter>=1.7.2,<2.0.0',
 'more-itertools>=8.12.0,<9.0.0',
 'progress>=1.6,<2.0',
 'pybids>=0.14.0,<0.15.0',
 'snakemake>=5.28.0',
 'typing-extensions>=3.10.0,<4.0.0']

entry_points = \
{'console_scripts': ['snakebids = snakebids.admin:main']}

setup_kwargs = {
    'name': 'snakebids',
    'version': '0.5.0',
    'description': 'BIDS integration into snakemake workflows',
    'long_description': "\nsnakebids\n=========\n.. image:: https://readthedocs.org/projects/snakebids/badge/?version=latest\n  :target: https://snakebids.readthedocs.io/en/latest/?badge=latest\n  :alt: Documentation Status\n\nSnakemake + BIDS\n\nThis package allows you to build BIDS Apps using Snakemake. It offers:\n\n\n* Flexible data grabbing with PyBIDS, configurable solely by config file entries\n* Helper function for creating BIDS paths inside Snakemake workflows/rules\n* Command-line invocation of snakemake workflows with BIDS App compliance\n* Configurable argument parsing specified using the Snakemake workflow config\n* Execution either as command-line BIDS apps or via snakemake executable\n\nContributing\n============\n\nClone the git repository. Snakebids dependencies are managed with Poetry, which you'll need installed on your machine. You can find instructions on the `poetry website <https://python-poetry.org/docs/master/#installation>`_. Then, setup the development environment with the following commands::\n\n  poetry install\n  poetry run poe setup\n\nSnakebids uses `poethepoet <https://github.com/nat-n/poethepoet>`_ as a task runner. You can see what commands are available by running::\n\n    poetry run poe\n\nIf you wish, you can also run ``poe [[command]]`` directly by installing ``poethepoet`` on your system. Follow the install instructions at the link above.\n\nTests are done with ``pytest`` and can be run via::\n\n  poetry run pytest\n\nSnakebids uses pre-commit hooks (installed via the ``poe setup`` command above) to lint and format code (we use `black <https://github.com/psf/black>`_, `isort <https://github.com/PyCQA/isort>`_, `pylint <https://pylint.org/>`_ and `flake8 <https://flake8.pycqa.org/en/latest/>`_). By default, these hooks are run on every commit. Please be sure they all pass before making a PR.\n",
    'author': 'Ali Khan',
    'author_email': 'alik@robarts.ca',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/akhanf/snakebids',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<3.11',
}


setup(**setup_kwargs)
