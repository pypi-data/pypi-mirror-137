# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['dj_blacksmith',
 'dj_blacksmith.client',
 'dj_blacksmith.client._async',
 'dj_blacksmith.client._sync']

package_data = \
{'': ['*']}

install_requires = \
['Django>=3.2,<=5',
 'aioredis>=2.0.1,<3.0.0',
 'blacksmith[prometheus]>=0.13.3,<0.14.0',
 'redis>=4.1.2,<5.0.0',
 'types-setuptools>=57.4.7,<58.0.0']

setup_kwargs = {
    'name': 'dj-blacksmith',
    'version': '0.2.0',
    'description': 'Django Bindings for Blacksmith',
    'long_description': 'dj-blacksmith\n=============\n\n.. image:: https://readthedocs.org/projects/dj-blacksmith/badge/?version=latest\n   :target: https://dj-blacksmith.readthedocs.io/en/latest/?badge=latest\n   :alt: Documentation Status\n\n.. image:: https://github.com/mardiros/dj-blacksmith/actions/workflows/main.yml/badge.svg\n   :target: https://github.com/mardiros/dj-blacksmith/actions/workflows/main.yml\n   :alt: Continuous Integration\n\n.. image:: https://codecov.io/gh/mardiros/dj-blacksmith/branch/main/graph/badge.svg?token=GMCE9HQE98\n   :target: https://codecov.io/gh/mardiros/dj-blacksmith\n   :alt: Coverage\n\nDjango bindings for `Blacksmith`_ rest api client.\n\n.. _`Blacksmith`: https://python-blacksmith.readthedocs.io/en/latest/index.html\n',
    'author': 'Guillaume Gauvrit',
    'author_email': 'guillaume@gauvr.it',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mardiros/dj-blacksmith',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
