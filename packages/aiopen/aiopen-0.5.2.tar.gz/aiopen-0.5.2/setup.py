# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['aiopen']

package_data = \
{'': ['*']}

install_requires = \
['funkify>=0.4.0,<0.5.0', 'xtyping>=0.5.0,<0.6.0']

setup_kwargs = {
    'name': 'aiopen',
    'version': '0.5.2',
    'description': 'Async file io',
    'long_description': None,
    'author': 'jesse',
    'author_email': 'jesse@dgi.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dynamic-graphics-inc/dgpy-libs/tree/master/libs/aiopen',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
