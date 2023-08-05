# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['poetry_git_auto_version']

package_data = \
{'': ['*']}

install_requires = \
['poetry>=1.2,<2.0']

entry_points = \
{'poetry.plugin': ['git-auto-version = '
                   'poetry_git_auto_version.plugin:GitAutoVersionPlugin']}

setup_kwargs = {
    'name': 'poetry-git-auto-version',
    'version': '1.0.0',
    'description': 'A Poetry plugin to auto-append commit count to git versions.',
    'long_description': 'None',
    'author': 'Joshua Butt',
    'author_email': 'josh@joshb.in',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
