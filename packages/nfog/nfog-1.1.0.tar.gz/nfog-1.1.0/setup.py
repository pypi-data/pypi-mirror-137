# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nfog', 'nfog.artwork', 'nfog.templates', 'nfog.tracks']

package_data = \
{'': ['*']}

install_requires = \
['appdirs>=1.4.4,<2.0.0',
 'cinemagoer>=2022.1.26,<2023.0.0',
 'click-default-group>=1.2.2,<2.0.0',
 'click>=8.0.3,<9.0.0',
 'jsonpickle>=2.1.0,<3.0.0',
 'langcodes[data]>=3.3.0,<4.0.0',
 'pyd2v>=1.3.0,<2.0.0',
 'pymediainfo>=5.1.0,<6.0.0',
 'requests>=2.27.1,<3.0.0',
 'tmdbsimple>=2.9.1,<3.0.0']

entry_points = \
{'console_scripts': ['nfo = nfog.nfog:cli']}

setup_kwargs = {
    'name': 'nfog',
    'version': '1.1.0',
    'description': 'Scriptable Database-Driven NFO Generator for Movies and TV.',
    'long_description': "# nfog\n\n[![License](https://img.shields.io/github/license/rlaphoenix/nfog)](https://github.com/rlaphoenix/nfog/blob/master/LICENSE)\n[![Python Support](https://img.shields.io/pypi/pyversions/nfog)](https://pypi.python.org/pypi/nfog)\n[![Release](https://img.shields.io/pypi/v/nfog)](https://pypi.python.org/pypi/nfog)\n[![GitHub issues](https://img.shields.io/github/issues/rlaphoenix/nfog)](https://github.com/rlaphoenix/nfog/issues)\n\nScriptable Database-Driven NFO Generator for Movies and TV.\n\n## Installation\n\n    pip install --user nfog\n\n## Building\n\n### Dependencies\n\n- [Python](https://python.org/downloads) (v3.7 or newer)\n- [Poetry](https://python-poetry.org/docs) (latest recommended)\n\n### Installation\n\n1. `git clone https://github.com/rlaphoenix/nfog`\n2. `cd nfog`\n3. `poetry config virtualenvs.in-project true` (optional, but recommended)\n4. `poetry install`\n5. `nfo -h`\n\n## Creating Templates\n\nWe use Template's to define the structure and logic that creates your NFO file. Your Template file may\ncreate NFOs of any kind of encoding or style, including ASCII, ANSI, and such. You don't have to conform\nto any specifications of any kind, but are encouraged to if possible.\n\nTo create a Template file, you simply need to inherit the `Template` class in `nfog.template`, fill out\nthe various abstract methods/properties, and create an `nfo` property that returns a final string.\n\nTake a look at the [Example Templates](/examples/templates) for pre-made examples for various NFO\nusage scenarios. You may modify these Templates in any way you like.\n\nNote: While you have complete freedom with what Python code you run from within the template, this also\nmeans you should not immediately trust template file as they are after all still Python files.\n\n## Creating Artwork\n\nJust like Templates, we use Artwork files to define the look and style of the surrounding NFO.\nYou may also do introspection of the NFO output to merge style within the contents of the NFO as well.\n\nTo create an Artwork file, inherit the `Artwork` class in `nfog.artwork`, fill out any abstract methods\nand properties, and create the `with_template` function that returns the final string containing both\nthe NFO output (from `template` argument) and the Artwork.\n\nTake a look at the [Example Artwork](/examples/artwork) to see how these are used. However, you cannot\nre-use these, or make derivative works. Please see the [Artwork License](/examples/artwork/LICENSE)\nfor more information.\n\n## Using Templates and Artwork\n\nTo use Templates and Artwork, calling `nfo` (or `nfo generate`) will ask you for various information, but\none of them is a Template to use. The Templates it makes available to use are loaded from the user templates\ndirectory which can be found by typing `nfo version`.\n\nTo use an Artwork, specify the name of the Artwork file (case-sensitive) to `-a/--artwork`.\nUsing an Artwork is completely optional.\n\nFor more information on using `nfog`, see the usage help by calling `nfo --help`.\n\n## License\n\n[Apache License, Version 2.0](LICENSE)\n",
    'author': 'PHOENiX',
    'author_email': 'rlaphoenix@pm.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/rlaphoenix/nfog',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
