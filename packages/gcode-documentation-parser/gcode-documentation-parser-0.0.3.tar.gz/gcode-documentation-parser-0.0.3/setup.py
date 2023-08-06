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
    'version': '0.0.3',
    'description': 'A utility that parses the documentation pages from Marlin, RepRap, and Klipper, to generate an index of commands usage',
    'long_description': 'gcode-documentation-parser\n==\n\nSee a [demo] usage of the output\n\nA utility that parses the documentation pages from Marlin, RepRap, and Klipper,\nto generate an index of commands usage.\n\nNormally, the output would be used by something like [gcode-documentation], to\nallow users to search and understand how a GCode command should be used.\n\nThis was originally created in [Octoprint] plugin [MarlinGcodeDocumentation],\nand needs the parsed documentation data to function.\n\n[demo]:https://costas-basdekis.github.io/gcode-documentation\n[gcode-documentation]:https://github.com/costas-basdekis/gcode-documentation\n[Octoprint]:https://octoprint.org/\n[MarlinGcodeDocumentation]:https://plugins.octoprint.org/plugins/marlingcodedocumentation/\n\n![](docs/marlin-gcode-documentation.png)\n',
    'author': 'Costas Basdekis',
    'author_email': 'code@basdekis.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://costas-basdekis.github.io/gcode-documentation-parser',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
