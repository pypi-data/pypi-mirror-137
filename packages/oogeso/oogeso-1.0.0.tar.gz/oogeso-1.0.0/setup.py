# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['oogeso',
 'oogeso.core',
 'oogeso.core.devices',
 'oogeso.core.networks',
 'oogeso.dto',
 'oogeso.io',
 'oogeso.plots',
 'oogeso.utils']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'Pyomo>=6.1.2,<7.0.0',
 'networkx>=2.6.3,<3.0.0',
 'numpy>=1.21.4,<2.0.0',
 'pandas>=1.3.4,<2.0.0',
 'pyarrow>=6.0.1,<7.0.0',
 'pydantic>=1.9.0,<2.0.0',
 'pydot>=1.4.2,<2.0.0',
 'scipy>=1.7.2,<2.0.0',
 'tqdm>=4.62.3,<5.0.0',
 'xlrd>=2.0.1,<3.0.0']

setup_kwargs = {
    'name': 'oogeso',
    'version': '1.0.0',
    'description': 'Offshore Oil and Gas Field Energy System Operational Optimisation (OOGESO)',
    'long_description': '<p>\n<a href="https://badge.fury.io/gh/oogeso%2Foogeso"><img src="https://badge.fury.io/gh/oogeso%2Foogeso.svg" alt="GitHub version" height="18"></a>\n<a href="https://github.com/oogeso/oogeso/actions/workflows/build.yml?query=workflow%3ACI"><img src="https://img.shields.io/github/workflow/status/oogeso/oogeso/CI" alt="Badge"></a>\n<a href="https://www.python.org/"><img src="https://img.shields.io/badge/python-3.7%20%7C%203.8%20%7C%203.9%20%7C%203.10-blue.svg" alt="Badge"></a>\n<a href="https://github.com/psf/black"><img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Badge"></a>\n<a href="https://lgtm.com/projects/g/oogeso/oogeso/alerts/"><img alt="Total alerts" src="https://img.shields.io/lgtm/alerts/g/oogeso/oogeso.svg?logo=lgtm&logoWidth=18"/></a>\n<a href="https://lgtm.com/projects/g/oogeso/oogeso/context:python"><img src="https://img.shields.io/lgtm/grade/python/g/oogeso/oogeso.svg?logo=lgtm&logoWidth=18" alt="Badge"></a>\n</p>\n<br/>\n\n# Offshore Oil and Gas Energy System Operational Optimisation Model (oogeso)\n\nPython module for modelling and analysing the energy system of offshore oil and gas fields, with renewable energy and storage integration.\n\nPart of the [Low Emission Centre](https://www.sintef.no/en/projects/lowemission-research-centre/) (SP5).\n\n## Getting started\nInstall latest Oogeso release from PyPi:\n```\npip install oogeso\n```\n\nin order to use the plotting functionality you will need to install plotting libraries:\n\n```\npip install matplotlib plotly seaborn\n```\n\n## User guide and examples\nThe online user guide  gives more information about how to\nspecify input data and run a simulation case.\n\n*  [User guide](https://oogeso.github.io/oogeso/)\n\n\n## Local installation\nPrerequisite: \n- [Poetry](https://python-poetry.org/docs/#installation)\n- [Pre-commit](https://pre-commit.com/)\n- [CBC solver](https://projects.coin-or.org/Cbc)\nClone or download the code and install it as a python package. I.e. navigate to the folder with the MANIFEST.in file and type:\n\n### Install dependencies\n1. `git clone git@github.com:oogeso/oogeso.git`\n2. `cd oogeso`\n3. `poetry install --no-root`  --no-root to not install the package itself, only the dependencies.\n4. `poetry shell`\n5. `poetry run pytest tests`\n\n### Local development in Docker\nAlternatively you can run and develop the code using docker and the Dockerfile in the root folder.\n\n### GitHub Actions Pipelines\n4 pipelines are defined.\n\n1. Build: Building and testing on multiple OS and python versions. Triggered on any push to GitHub.\n2. CBC-optimizer CI: Build and test oogeso with the CBC-solver and spesific cbc-tests.\n3. Release: Create release based on tags starting on v*.\n4. Publish: Publish the package to PyPi when a release is marked as published.\n\n## Contribute\nYou are welcome to contribute to the improvement of the code.\n\n* Use Issues to describe and track needed improvements and bug fixes\n* Use branches for development and pull requests to merge into main\n* Use [Pre-commit hooks](https://pre-commit.com/)\n\n### Contact\n\n[Harald G Svendsen](https://www.sintef.no/en/all-employees/employee/?empid=3414)  \nSINTEF Energy Research\n',
    'author': 'Harald Svendsen',
    'author_email': 'harald.svendsen@sintef.no',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/oogeso/oogeso',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<3.11',
}


setup(**setup_kwargs)
