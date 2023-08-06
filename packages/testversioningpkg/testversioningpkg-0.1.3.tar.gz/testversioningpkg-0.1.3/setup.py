# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['testversioningpkg',
 'testversioningpkg.customs.event_a',
 'testversioningpkg.customs.event_b',
 'testversioningpkg.versions',
 'testversioningpkg.versions.v1',
 'testversioningpkg.versions.v2',
 'testversioningpkg.versions.v3',
 'testversioningpkg.versions.v4']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'testversioningpkg',
    'version': '0.1.3',
    'description': 'Test versioning package',
    'long_description': None,
    'author': 'Marchandev',
    'author_email': 'dhiva.hanifsyah@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
