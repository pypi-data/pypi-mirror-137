# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['finorch',
 'finorch.client',
 'finorch.config',
 'finorch.sessions',
 'finorch.sessions.local',
 'finorch.sessions.ozstar',
 'finorch.transport',
 'finorch.utils',
 'finorch.wrapper']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy>=1.4.29,<2.0.0',
 'appdirs>=1.4.4,<2.0.0',
 'exc>=0.92,<0.93',
 'finesse>=3.0a2,<4.0',
 'paramiko>=2.9.2,<3.0.0']

setup_kwargs = {
    'name': 'finorch',
    'version': '0.1.2',
    'description': 'Finesse version 3 job orchestrator and manager. This package can be used to run parallel jobs on various remote platforms, as well as locally.',
    'long_description': None,
    'author': 'Lewis Lakerink',
    'author_email': 'llakerink@swin.edu.au',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
