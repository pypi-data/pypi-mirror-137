# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mozci',
 'mozci.console',
 'mozci.console.commands',
 'mozci.data',
 'mozci.data.sources',
 'mozci.data.sources.artifact',
 'mozci.data.sources.bugbug',
 'mozci.data.sources.hgmo',
 'mozci.data.sources.taskcluster',
 'mozci.data.sources.treeherder',
 'mozci.util']

package_data = \
{'': ['*']}

install_requires = \
['ValidX>=0.7,<0.8',
 'appdirs>=1,<2',
 'cachy>=0,<1',
 'cleo>=0.8.1,<0.9.0',
 'flake8>=3,<5',
 'loguru>=0,<1',
 'lru-dict>=1.1.7,<2.0.0',
 'pyyaml>=5,<6',
 'requests>=2,<3',
 'tabulate>=0.8.9,<0.9.0',
 'taskcluster>=38',
 'taskcluster_urls>=13,<14',
 'tomlkit>=0,<1']

extras_require = \
{':extra == "cache" or extra == "cache-seeded-file"': ['zstandard>=0,<1'],
 'adr': ['adr>=0,<1'],
 'cache': ['boto3>=1,<2', 'python3-memcached>=1,<2', 'redis>=3,<4'],
 'cache-memcached': ['python3-memcached>=1,<2'],
 'cache-redis': ['redis>=3,<4'],
 'cache-s3': ['boto3>=1,<2']}

entry_points = \
{'console_scripts': ['mozci = mozci.console.application:cli']}

setup_kwargs = {
    'name': 'mozci',
    'version': '2.1.0',
    'description': '',
    'long_description': None,
    'author': 'Andrew Halberstadt',
    'author_email': 'ahal@mozilla.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4',
}


setup(**setup_kwargs)
