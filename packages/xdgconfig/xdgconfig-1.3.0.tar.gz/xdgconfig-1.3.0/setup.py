# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['xdgconfig', 'xdgconfig.cli_tools', 'xdgconfig.serializers']

package_data = \
{'': ['*']}

install_requires = \
['mergedeep>=1.3.4,<2.0.0']

setup_kwargs = {
    'name': 'xdgconfig',
    'version': '1.3.0',
    'description': 'Easy access to `~/.config`',
    'long_description': "# XDGConfig\n\n[![Discord](https://img.shields.io/discord/812645240611536906?label=&logo=discord&logoColor=ffffff&color=7389D8&labelColor=6A7EC2)](https://discord.gg/kDgyr9Uzwj)\n[![GitHub license](https://img.shields.io/github/license/Dogeek/xdgconfig.svg)](https://github.com/Dogeek/xdgconfig/blob/master/LICENSE)\n[![PyPI version shields.io](https://img.shields.io/pypi/v/xdgconfig.svg)](https://pypi.python.org/pypi/xdgconfig/)\n[![PyPI pyversions](https://img.shields.io/pypi/pyversions/xdgconfig.svg)](https://pypi.python.org/pypi/xdgconfig/)\n\nEasy access to `~/.config`.\n\n\n## Installation\n\n### Using pip\n\nSimply run `pip3 install --upgrade xdgconfig`.\n\nBy default, `xdgconfig` only supports JSON as its serializer, but you can install support for\nother serializers by specifiying the format in square brackets, i.e. `pip3 install xdgconfig[xml]`.\nThe following are available:\n\n- `jsonc`: JSON, with comments\n- `ini`: INI files\n- `xml`: eXtensible Markup Language files\n- `toml`: Tom's Markup language files\n- `yaml`: YAML Ain't Markup Language files\n\nFurthermore there is an `all` recipe to install support for every markup supported,\nand you can combine them by using a `+` between 2 targets, i.e. `pip3 install xdgconfig[xml+toml]`\n\n### From source\n\nSimply clone this repo and run `python3 setup.py install`.\n\n## Features\n\n- `Config` objects use a shared single reference.\n- Serializing to many common formats, including JSON, XML, TOML, YAML, and INI\n- `dict`-like interface\n- Autosaving on mutation of the `Config` object.\n- Smart config loading, especially on Unix-based platforms\n  - looks in `/etc/prog/config`, then in `~/.config/prog/config`\n  - Supports setting a config file path in an environment variable named `PROG_CONFIG_PATH`\n- Accessing the config using dot notation (`config.key` for instance). See limitations for guidance.\n\n\n## Usage\n\n```python\nfrom xdgconfig import JsonConfig\n\n# Instanciate the JsonConfig object\n# If you'd rather use a different format, there also are config classes\n# for TOML, YAML, INI (configparser), and XML.\n# This will save your configuration under `~/.config/PROG/config\nconfig = JsonConfig('PROG', autosave=True)\n\nconfig['foo'] = 'bar'  # Save a value to the config\n\n# Access the value later on\nprint(config['foo'])\n\n# It behaves like a collections.defaultdict as well\nconfig['oof']['bar'] = 'baz'\n\n# Prints {'oof': {'bar': 'baz'}, 'foo': 'bar'}\nprint(config)\n\n```\n\n## Adding onto the library\n\n### Custom serializers\n\nYou can add custom serializers support by using a Mixin class, as well as\na serializer class which must have a `dumps` and a `loads` method, which will\nbe used to store and load data from the config file. The data is always\nrepresented as a python `dict` object, but you can serialize any data you want\ninside of it.\n\nLook at the following example for an implementation guide.\n\n```python\nfrom typing import Any, Dict\n\nfrom xdgconfig import Config\n\n\nclass MySerializer:\n    def dumps(data: Dict[str, Any]) -> str:\n        return '\\n'.join(f'{k}:{v}' for k, v in data.items())\n\n    def loads(contents: str) -> Dict[str, Any]:\n        return dict(s.split(':') for s in contents.split('\\n'))\n\n\nclass MySerializerMixin:\n    _SERIALIZER = MySerializer\n\n\nclass MyConfig(MySerializerMixin, Config):\n    ...\n\n```\n\n### Setting default values\n\nYou can set default values by creating a `Mixin` class with a `_DEFAULTS` class attribute, such as :\n\n```python\nfrom pathlib import Path\nfrom pprint import pprint\n\nfrom xdgconfig import JsonConfig\n\n\nclass DefaultConfig:\n    _DEFAULTS = {\n        'logger.level': 'info',\n        'logger.verbosity': 3,\n        'app.path': str(Path.cwd()),\n        'app.credentials.username': 'user',\n        'app.credentials.password': 'password',\n    }\n\n\nclass Config(DefaultConfig, JsonConfig):\n    ...\n\n\nconfig = Config('PROG', 'config.json')\npprint(config)\n# Prints the following dict :\n# {\n#     'logger': {\n#         'level': 'info',\n#         'verbosity': 3\n#     },\n#     'app': {\n#         'path': '$CWD',\n#         'credentials': {\n#             'username': 'user',\n#             'password': 'password'\n#         }\n#     }\n# }\n\n```\n\n\n## Known limitations\n\n- Using an `IniConfig` object prevents you from using periods (`.`) in key names, as they are separators for subdicts.\n- Methods and attributes of the `Config` object all start with a leading underscore (`_`), hence, using key names with the same convention is discouraged, as it could break the object due to the way dot (`.`) accessing works. The only exception is the `save` method, which doesn't start with a leading underscore.\n- There can only be one document per config file, and a config file is a dictionary.\n- Depending on the serializer used, some data types may or may not be available. You can circumvent that by using custom serializers.\n- Configuration files with comments will have their comments dropped when the configuration is saved.\n",
    'author': 'Dogeek',
    'author_email': 'Dogeek@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Dogeek/xdgconfig',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
