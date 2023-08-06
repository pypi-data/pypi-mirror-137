# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['datalake_catalog', 'datalake_catalog.schemas']

package_data = \
{'': ['*'], 'datalake_catalog': ['config/*']}

install_requires = \
['Flask-JWT-Extended>=4.3.1,<5.0.0',
 'Flask>=2.0.2,<3.0.0',
 'click>=8.0.3,<9.0.0',
 'gunicorn>=20.1.0,<21.0.0',
 'jsonschema>=4.2.1,<5.0.0',
 'pony>=0.7.14,<0.8.0']

entry_points = \
{'console_scripts': ['catalog = datalake_catalog.main:cli']}

setup_kwargs = {
    'name': 'datalake-catalog',
    'version': '1.0.1',
    'description': 'Datalake Catalog',
    'long_description': None,
    'author': 'Didier SCHMITT',
    'author_email': 'dschmitt@equancy.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://git.equancy.cloud/equancy/data-technologies/datalake-catalog',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
