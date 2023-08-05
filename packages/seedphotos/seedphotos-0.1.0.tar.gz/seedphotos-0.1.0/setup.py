# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['seedphotos']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.27.1,<3.0.0']

setup_kwargs = {
    'name': 'seedphotos',
    'version': '0.1.0',
    'description': 'A lib that create image through words',
    'long_description': None,
    'author': 'Vinicius Barbosa de Aguiar',
    'author_email': 'vb9763662@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
