# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['clicksignlib',
 'clicksignlib.adapters',
 'clicksignlib.environments',
 'clicksignlib.environments.protocols',
 'clicksignlib.handlers',
 'clicksignlib.handlers.document_handler',
 'clicksignlib.handlers.embedded_handler',
 'clicksignlib.handlers.mixins',
 'clicksignlib.handlers.notification_handler',
 'clicksignlib.handlers.signatory_handler',
 'clicksignlib.handlers.template_handler',
 'clicksignlib.utils',
 'clicksignlib.utils.errors',
 'clicksignlib.utils.validators']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.1,<4.0.0', 'httpx>=0.21.1,<0.22.0']

setup_kwargs = {
    'name': 'clicksignlib',
    'version': '1.1.4',
    'description': '',
    'long_description': None,
    'author': 'Erick Duarte',
    'author_email': 'erickod@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
