# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['strangeworks',
 'strangeworks.annealing',
 'strangeworks.auth',
 'strangeworks.errors',
 'strangeworks.rest_client']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.4.3,<4.0.0',
 'pylatexenc==2.7',
 'pyyaml>=5.4.1,<6.0.0',
 'requests==2.26.0']

setup_kwargs = {
    'name': 'strangeworks',
    'version': '0.2.2',
    'description': 'Strangeworks core',
    'long_description': '| ⚠️    | This SDK is currently in pre-release alpha state and subject to change. To get more info or access to test features check out the [Strangeworks Backstage Pass Program](https://strangeworks.com/backstage). |\n|---------------|:------------------------|\n\n# Strangeworks SDK\n\nPython SDK granting easy access to the Strangeworks API. For more information on using the SDK check out the [Strangeworks docs](https://docs.strangeworks.com/).',
    'author': 'Strange Devs',
    'author_email': 'stranger@strangeworks.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
