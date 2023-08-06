# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kg_detective',
 'kg_detective.de',
 'kg_detective.de.rules',
 'kg_detective.en',
 'kg_detective.en.rules',
 'kg_detective.es',
 'kg_detective.es.rules']

package_data = \
{'': ['*']}

install_requires = \
['spacy>=3.2.0,<4.0.0']

setup_kwargs = {
    'name': 'kg-detective',
    'version': '0.1.4',
    'description': '',
    'long_description': None,
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
