# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gcode_documentation_parser']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4,<4.10.0', 'wikitextparser>=0.45.2,<0.46.0']

setup_kwargs = {
    'name': 'gcode-documentation-parser',
    'version': '0.0.1',
    'description': '',
    'long_description': None,
    'author': 'Costas Basdekis',
    'author_email': 'costas.basdekis@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
