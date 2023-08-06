# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['tft', 'tft.nucleus.api', 'tft.nucleus.api.routers', 'tft.nucleus.api.schemes']

package_data = \
{'': ['*']}

install_requires = \
['alembic>=1.6.5,<2.0.0',
 'cockroachdb>=0.3.5,<0.4.0',
 'cryptography>=3.4.7,<4.0.0',
 'dynaconf>=3.1.7,<4.0.0',
 'fastapi-versioning>=0.8.0,<0.9.0',
 'fastapi>=0.66,<0.67',
 'gunicorn>=20.0.4,<21.0.0',
 'psycopg2-binary>=2.9.1,<3.0.0',
 'requests>=2.25.1,<3.0.0',
 'sentry-sdk>=1.5.1,<2.0.0',
 'sqlalchemy-cockroachdb>=1.4.0,<2.0.0',
 'sqlalchemy-utils>=0.37.6,<0.38.0',
 'sqlalchemy>=1.3.2,<2.0.0',
 'uvicorn>=0.13,<0.14']

setup_kwargs = {
    'name': 'tft-api',
    'version': '0.0.2',
    'description': 'Testing Farm Core - public and internal API',
    'long_description': None,
    'author': 'Evgeny Fedin',
    'author_email': 'efedin@redhat.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
