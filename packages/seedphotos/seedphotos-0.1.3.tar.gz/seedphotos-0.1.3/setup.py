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
    'version': '0.1.3',
    'description': 'A lib that create image through words',
    'long_description': "# SeedPhotos\n\n<p>A lib that create image through words</p>\n\n## Install:\n\n<p>Use poetry or pip for installation: </p>\n\n    pip install seedphotos\n\nor\n\n    poetry add seedphotos\n\n\n\n## How to use:\n\n```python\nfrom seedphotos.photos import *\n\n    photos = Photos(width=300, height=300, filename='image name', seed='word seed', folder='file folder', format='webp or jpg') # Mandatory parameters to generate the image\n    photos.getPhotos() # Download image\n```\n\n<p>With all parameters satisfied it looks like this: </p>\n\n```python\nfrom seedphotos.photos import *\n\nphotos = Photos(width=300, height=300, filename='image', seed='Brazil', folder='/home/barbosa/test/test', format='jpg')\nphotos.getPhotos()\n```",
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
