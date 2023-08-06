# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mc_converter', 'mc_converter.Helpers']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.7.4,<4.0.0',
 'murmurhash2>=0.2.9,<0.3.0',
 'pytoml>=0.1.21,<0.2.0',
 'tenacity>=8.0.1,<9.0.0',
 'tomli>=1.2.1,<2.0.0']

entry_points = \
{'console_scripts': ['mc-converter = mc_converter:main']}

setup_kwargs = {
    'name': 'mc-converter',
    'version': '1.0.3',
    'description': '',
    'long_description': "# modpack-converter\nConvert's one minecraft modpack format to another.\n\nMaybe I need to think of a better name...\n\n# Features\n\n- Auto detect input modpack format\n- Support convertions to and from:\n    - MultiMC (parsing only)\n    - CurseForge\n    - Modrinth\n    - packwiz\n- Detects downloadable resourcepacks and shaders (MultiMC only)\n- User friendly toml config\n- Multiple output formats at once\n\n# How to Use\n\n```\nmc-converter [-h] [-c CONFIG] -i INPUT -f FORMAT [-o OUTPUT]\n```\n\n## Explanation:\n\n```\n-h --help: prints help\n-i --input: specifies input file (mostly zip file)\n-c --config: specifies config file, used for fill the gaps like description or files not in modrinth on curseforge example can be found in this repository.\n-f --format: soecifies formats to convert, must be separated by space.\n-o --output: specifies output directory, where converted zip files will be stored. By default current working directory will be used.\n```\n\nAvaliable formats:     - `curseforge, modrinth, packwiz, intermediate`\n\n`intermediate` must be used only for debuging, can contain sensetive information\n\nExample: \n```\nmc-converter -i MyLovelyMultiMcModpack.zip -c config.toml -f curseforge modrinth -o converted_modpacks\n```\n\n# How to Install\n\n## From PyPI\n```\npip install mc-converter\n```\n## From `.whl` file\nGo to Release page, download latest `.whl` file \\\n And install it via the following comand:\n ```\n pip install mc_converter_{version}.whl\n ```\n \n # Credits\n\nmurmurhash2 - Murmur Hash 2 libray - https://pypi.org/project/murmurhash2 \\\naiohttp - Async web interface - https://github.com/aio-libs/aiohttp \\\ntomli - Fast pure python toml parser - https://github.com/hukkin/tomli \\\npytoml - The only one toml writer that can handle weird packwiz files - https://github.com/avakar/pytoml",
    'author': 'RozeFound',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/RozeFound/modpack-converter',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
