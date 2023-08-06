# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['datek_jaipur',
 'datek_jaipur.application',
 'datek_jaipur.application.adapters',
 'datek_jaipur.application.adapters.console',
 'datek_jaipur.application.state_machine',
 'datek_jaipur.domain',
 'datek_jaipur.domain.compound_types',
 'datek_jaipur.domain.errors',
 'datek_jaipur.domain.events']

package_data = \
{'': ['*']}

install_requires = \
['datek-async-fsm>=0.2.0,<0.3.0']

entry_points = \
{'console_scripts': ['run-console-app = datek_jaipur.application.console:main']}

setup_kwargs = {
    'name': 'datek-jaipur',
    'version': '0.1.1',
    'description': "Implementation of Jaipur board game's logic",
    'long_description': '[![codecov](https://codecov.io/gh/DAtek/datek-jaipur/branch/master/graph/badge.svg?token=8ET11QQUKN)](https://codecov.io/gh/DAtek/datek-jaipur)\n<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>\n<a href="https://github.com/psf/black/blob/main/LICENSE"><img alt="License: MIT" src="https://black.readthedocs.io/en/stable/_static/license.svg"></a>\n\n# Jaipur board game\n\nThe game rules are implemented in *Domain Driven* -ish fashion.  \nA custom finite state machine is the driver and there is a console adapter available for it.\n\n### Usage \n\n- Run the game with `run-console-app`\n',
    'author': 'Attila Dudas',
    'author_email': 'dudasa7@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/DAtek/datek-jaipur',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
