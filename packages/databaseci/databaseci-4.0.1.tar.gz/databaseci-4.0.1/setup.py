# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['databaseci']

package_data = \
{'': ['*']}

install_requires = \
['click', 'console', 'migra', 'psycopg2-binary', 'py', 'pyyaml', 'requests']

entry_points = \
{'console_scripts': ['databaseci = databaseci:command.cli']}

setup_kwargs = {
    'name': 'databaseci',
    'version': '4.0.1',
    'description': 'databaseci.com client',
    'long_description': '## Go to [databaseci.com](https://databaseci.com/) for more details.\n',
    'author': 'Robert Lechte',
    'author_email': 'rob@databaseci.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://databaseci.com',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4',
}


setup(**setup_kwargs)
