# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rest_serializer_to_typescript',
 'rest_serializer_to_typescript.management',
 'rest_serializer_to_typescript.management.commands',
 'rest_serializer_to_typescript.tests']

package_data = \
{'': ['*']}

install_requires = \
['djangorestframework>=3.12.4,<4.0.0']

setup_kwargs = {
    'name': 'rest-serializer-to-typescript',
    'version': '0.2.0',
    'description': '',
    'long_description': None,
    'author': 'Abdollah Keshtkar',
    'author_email': 'hamadkeshtkar@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
