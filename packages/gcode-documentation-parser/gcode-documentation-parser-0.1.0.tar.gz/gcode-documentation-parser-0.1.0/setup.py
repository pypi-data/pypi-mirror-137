# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gcode_documentation_parser',
 'gcode_documentation_parser.parser',
 'gcode_documentation_parser.parser.parsers']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4,<4.10.0', 'wikitextparser>=0.45.2,<0.46.0']

setup_kwargs = {
    'name': 'gcode-documentation-parser',
    'version': '0.1.0',
    'description': 'A utility that parses the documentation pages from Marlin, RepRap, and Klipper, to generate an index of commands usage',
    'long_description': 'gcode-documentation-parser\n==\n\nSee a [demo] usage of the output\n\nA utility that parses the documentation pages from Marlin, RepRap, and Klipper,\nto generate an index of commands usage.\n\nOutput\n--\n\nYou can access the output from the [output branch] of this repo. Here are the\nraw links that you can reference or copy:\n\n* [all_codes.json]: A JSON file containing the documentation\n* [all_codes_window.js]: A JS file that defines `AllGcodes` on the global\n* `window` object\n* [all_codes_const.js]: A JS file that defines a `const AllGcodes`\n* [all_codes_export.js]: A JS file that exports an `AllGcodes` value\n\nThe documentation is updated semi-regularly, at the start of every month, and\npublished on this repo.\n\nYou can also generate it locally by running the following, and checking the\n`output` folder\n\n```shell\npoetry run ./update_documentation.py\n```\n\nUsage\n--\n\nNormally, the output would be used by something like [gcode-documentation], to\nallow users to search and understand how a GCode command should be used.\n\nThis was originally created in [Octoprint] plugin [MarlinGcodeDocumentation],\nand needs the parsed documentation data to function.\n\n[demo]:https://costas-basdekis.github.io/gcode-documentation\n[output branch]:https://github.com/costas-basdekis/gcode-documentation-parser/tree/output\n[all_codes.json]:https://raw.githubusercontent.com/costas-basdekis/gcode-documentation-parser/output/output/all_codes.json\n[all_codes_window.js]:https://raw.githubusercontent.com/costas-basdekis/gcode-documentation-parser/output/output/all_codes_window.js\n[all_codes_const.js]:https://raw.githubusercontent.com/costas-basdekis/gcode-documentation-parser/output/output/all_codes_const.js\n[all_codes_export.js]:https://raw.githubusercontent.com/costas-basdekis/gcode-documentation-parser/output/output/all_codes_export.js\n[gcode-documentation]:https://github.com/costas-basdekis/gcode-documentation\n[Octoprint]:https://octoprint.org/\n[MarlinGcodeDocumentation]:https://plugins.octoprint.org/plugins/marlingcodedocumentation/\n\n![](docs/marlin-gcode-documentation.png)\n',
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
