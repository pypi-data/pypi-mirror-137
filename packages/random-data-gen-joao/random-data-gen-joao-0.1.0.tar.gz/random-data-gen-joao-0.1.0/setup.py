# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['random_data_gen_joao', 'random_data_gen_joao.features']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.22.1,<2.0.0', 'pandas>=1.4.0,<2.0.0']

setup_kwargs = {
    'name': 'random-data-gen-joao',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'João Paulo Nogueira',
    'author_email': 'joaonogueira@fisica.ufc.br',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
