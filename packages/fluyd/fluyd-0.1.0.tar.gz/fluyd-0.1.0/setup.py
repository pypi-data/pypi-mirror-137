# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fluyd']

package_data = \
{'': ['*']}

install_requires = \
['pylint[test]>=2.12.2,<3.0.0', 'pytest-cov[test]>=3.0.0,<4.0.0']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata>=1.0,<2.0']}

setup_kwargs = {
    'name': 'fluyd',
    'version': '0.1.0',
    'description': 'Include description',
    'long_description': None,
    'author': 'Gabriel Gazola Milan',
    'author_email': 'gabriel.gazola@poli.ufrj.br',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
