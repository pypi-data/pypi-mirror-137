# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pythonvcs']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.27.1,<3.0.0']

setup_kwargs = {
    'name': 'pythonvcs',
    'version': '0.0.1',
    'description': 'API wrapper for gitea, pijul nest, etc.',
    'long_description': None,
    'author': 'MisileLaboratory',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
