# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['floodlight', 'floodlight.core', 'floodlight.io', 'floodlight.utils']

package_data = \
{'': ['*']}

install_requires = \
['iso8601>=1.0.2,<2.0.0',
 'lxml>=4.6.4,<5.0.0',
 'numpy>=1.21.2,<2.0.0',
 'pandas>=1.3.4,<2.0.0',
 'pytz>=2021.3,<2022.0']

setup_kwargs = {
    'name': 'floodlight',
    'version': '0.2.1',
    'description': 'A high-level framework for sports data analysis',
    'long_description': "[version-image]: https://img.shields.io/pypi/v/floodlight?color=006666\n[version-url]: https://pypi.org/project/floodlight/\n[python-image]: https://img.shields.io/pypi/pyversions/floodlight?color=006666\n[python-url]: https://pypi.org/project/floodlight/\n[docs-image]: https://readthedocs.org/projects/floodlight/badge/?version=latest\n[docs-url]: https://floodlight.readthedocs.io/en/latest/?badge=latest\n[build-image]: https://github.com/floodlight-sports/floodlight/actions/workflows/build.yaml/badge.svg\n[build-url]: https://github.com/floodlight-sports/floodlight/actions/workflows/build.yaml\n[lint-image]: https://github.com/floodlight-sports/floodlight/actions/workflows/linting.yaml/badge.svg\n[lint-url]: https://github.com/floodlight-sports/floodlight/actions/workflows/linting.yaml\n[status-image]: https://img.shields.io/badge/status-beta-006666\n[status-url]: https://img.shields.io/badge/status-beta-006666\n[black-image]: https://img.shields.io/badge/code%20style-black-000000.svg\n[black-url]: https://github.com/psf/black\n[contrib-image]: https://img.shields.io/badge/contributions-welcome-006666\n[contrib-url]: https://github.com/floodlight-sports/floodlight/blob/main/CONTRIBUTING.md\n[institute-link]:\n\n# floodlight\n[![Latest Version][version-image]][version-url]\n[![Python Version][python-image]][python-url]\n[![Documentation Status][docs-image]][docs-url]\n[![Build Status][build-image]][build-url]\n[![Linting Status][lint-image]][lint-url]\n[![PyPI][status-image]][status-url]\n[![Code style: black][black-image]][black-url]\n\n\n## A high-level, data-driven sports analytics framework\n\n**floodlight** is a Python package for streamlined analysis of sports data. It is\ndesigned with a clear focus on scientific computing and built upon popular libraries\nsuch as *numpy* or *pandas*.\n\nLoad, integrate, and process tracking and event data, codes and other match-related\ninformation from major data providers. This package provides a set of  standardized\ndata objects to structure and handle sports data, together with a suite of common\nprocessing operations such as transforms or data manipulation methods.\n\nAll implementations run completely provider- and sports-independent, while maintaining\na maximum of flexibility to incorporate as many data flavours as possible. A high-level\ninterface allows easy access to all standard routines, so that you can stop worrying\nabout data wrangling and start focussing on the analysis instead!\n\n\n### Features\n\nThis project is still in its early childhood, and we hope to quickly expand the set\nof features in the future. At this point, we've implemented core data structures and\nparsing functionality for major data providers.\n\n#### Data objects\n\n- Data-level objects to store\n  - Tracking data\n  - Event data\n  - Pitch information\n  - Codes such as ball possession information\n\n#### Parser\n\n- ChyronHego\n  - Tracking data\n  - Codes\n- DFL\n  - Tracking data\n  - Codes\n  - Event data\n- Kinexon\n  - Tracking data\n- Opta\n  - Event data (f24 feeds)\n- Stats Perform\n  - Tracking data\n  - Event data\n\n\n### Installation\n\nThe package can be installed easily via pip:\n\n```\npip install floodlight\n```\n\n\n### Contributing [![Contributions][contrib-image]][contrib-url]\n\nCheck out [Contributing.md][contrib-url] for a quick rundown of what you need to\nknow to get started. We also provide an extended, beginner-friendly guide on how to\nstart contributing in our documentation.\n\n\n### Documentation\n\nYou can find all documentation [here][docs-url].\n\n\n### Why\n\nWhy do we need another package that introduces its own data structures and ways of dealing with certain problems? And,\nto be honest, what's the purpose of trying to integrate all these different files and fit them into a single framework?\nEspecially since there already exist packages that aim to solve certain parts of that pipeline?\n\nThe answer is, while we love those packages out there, that we did not find a solution that did fit our needs.\nAvailable packages are either tightly connected to a certain data format/provider, adapt to the subtleties of a\nparticular sport, or only solve *one* particular problem. This still left us with the essential problem of adapting to\nall those different interfaces.\n\nWe felt that as long as there is no underlying, high-level framework, each and every use case again and again needs its\nown implementation. At last, we found ourselves refactoring the same code - and there are certain processing or\nplotting routines that are required in *almost every* project - over and over again, just to fit the particular data\nstructures we were dealing with at that time.\n\n\n### About\n\nThis project has been kindly supported by the [Institute of Exercise Training and Sport\nInformatics](https://www.dshs-koeln.de/en/institut-fuer-trainingswissenschaft-und-sportinformatik/) at the German Sport\nUniversity Cologne under supervision of Prof. Daniel Memmert.\n\n\n### Related Projects\n\n- [matplotsoccer](https://github.com/TomDecroos/matplotsoccer)\n- [kloppy](https://github.com/PySport/kloppy)\n- [codeball](https://github.com/metrica-sports/codeball)\n",
    'author': 'draabe',
    'author_email': 'draabx@posteo.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/floodlight-sports/floodlight',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<3.11',
}


setup(**setup_kwargs)
