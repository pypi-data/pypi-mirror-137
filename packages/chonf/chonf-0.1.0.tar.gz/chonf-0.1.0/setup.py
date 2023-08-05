# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['chonf',
 'chonf.parsers',
 'chonf.parsers.env',
 'chonf.parsers.env.test',
 'chonf.parsers.json',
 'chonf.parsers.json.test',
 'chonf.parsers.toml',
 'chonf.parsers.toml.test',
 'chonf.test']

package_data = \
{'': ['*']}

install_requires = \
['toml>=0.10.2,<0.11.0']

setup_kwargs = {
    'name': 'chonf',
    'version': '0.1.0',
    'description': 'User config management made simple and powerful',
    'long_description': None,
    'author': 'João C. Rodrigues Jr.',
    'author_email': 'jc.rodrigues1997@usp.br',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
