# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['protomake']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.3,<9.0.0',
 'grpcio-tools>=1.43.0,<2.0.0',
 'mypy-protobuf>=3.2.0,<4.0.0']

setup_kwargs = {
    'name': 'protomake',
    'version': '0.1.1',
    'description': 'Generate .py from .proto.',
    'long_description': None,
    'author': 'Manuel Šarić',
    'author_email': 'manujelko@gmail.com',
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
