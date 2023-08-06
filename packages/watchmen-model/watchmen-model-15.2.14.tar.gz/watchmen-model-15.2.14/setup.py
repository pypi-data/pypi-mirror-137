# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['model',
 'model.model',
 'model.model.common',
 'model.model.console_space',
 'model.model.dashborad',
 'model.model.enum',
 'model.model.external',
 'model.model.pipeline',
 'model.model.report',
 'model.model.space',
 'model.model.topic']

package_data = \
{'': ['*']}

install_requires = \
['bson>=0.5.10,<0.6.0', 'pydantic>=1.8.2,<2.0.0']

setup_kwargs = {
    'name': 'watchmen-model',
    'version': '15.2.14',
    'description': '',
    'long_description': None,
    'author': 'luke0623',
    'author_email': 'luke0623@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
