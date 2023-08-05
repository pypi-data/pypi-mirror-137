# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['logpass_pytest_plugins', 'logpass_pytest_plugins.contrib']

package_data = \
{'': ['*']}

install_requires = \
['pytest>=5.4.0']

extras_require = \
{'auto_pytest_factoryboy': ['pytest-factoryboy>=2.1.0,<3.0.0'],
 'channels': ['channels>=3.0.0',
              'pytest-asyncio>=0.17.2,<0.18.0',
              'pytest-django>=4.5.2,<5.0.0'],
 'rest_framework': ['djangorestframework>=3.13.1,<4.0.0']}

entry_points = \
{'pytest11': ['auto_pytest_factoryboy = '
              'logpass_pytest_plugins.contrib.auto_pytest_factoryboy',
              'channels = logpass_pytest_plugins.contrib.channels',
              'rest_framework = logpass_pytest_plugins.contrib.rest_framework']}

setup_kwargs = {
    'name': 'logpass-pytest-plugins',
    'version': '0.0.2',
    'description': "Pytest's plugins crafted by LogPass",
    'long_description': "# LogPass pytest plugins\n\nA few pytest plugins used by LogPass.\n\n## Installation\n\nTo use `logpass_pytest_plugins` simply install it with your package manager,\ne.g. via pip:\n\n```bash\npip install logpass_pytest_plugins\n```\n\nTo install plugin with all its dependencies use one of following extras:\n\n+ `auto_pytest_factoryboy`\n+ `channels`\n+ `rest_framework`\n\nFor instance, to install `channels` and `rest_framework` plugins with all\ndependencies:\n\n```bash\npip install logpass_pytest_plugins[channels,rest_framework]\n```\n\n## Available plugins\n\nAll plugins are used by default (that's default `pytest` behaviour).\nIf you don't need some plugin (e.g. you don't use `djangorestframework`)\nsimply disable it for particular command call:\n\n```bash\npytest -p no:rest_framework\n```\n\nor do it in `pytest.ini` (or other file with `pytest` configuration):\n\n```ini\n[pytest]\naddopts = -p no:rest_framework\n```\n\n### `logpass_pytest_plugins.contrib.auto_pytest_factoryboy`\n\nPlugin that automatically registers `factory_boy` factories to\n`pytest-factoryboy`, so factories and models instances will be available\nas pytest fixtures.\n\n#### Configuration\n\nFollowing INI options can be used to configure `auto_pytest_factoryboy` plugin:\n\n+ `auto_pytest_factoryboy_root_dir` - directory where factories declarations\n  searching starts (defaults to `.` - pytest config path)\n+ `auto_pytest_factoryboy_globs` - list of `glob` patterns used to find files\n  with `factoryboy` factories declarations starting from the\n  `auto_pytest_factoryboy_root_dir` directory (defaults to `**/factories*.py`)\n\n### `logpass_pytest_plugins.contrib.channels`\n\nPlugin that simplifies `channels` consumers testing by providing following\nfixtures:\n\n+ `websocket_commmunicator_factory` - factory of `WebSocketCommunicator`\n  instances, that will automatically disconnect at the end of a test.\n  Using this fixture also automatically flush all used channel layers\n+ `http_commmunicator_factory` - factory of `HttpCommunicator`\n  instances. Using this fixture also automatically flush all used\n  channel layers\n\n### `logpass_pytest_plugins.contrib.rest_framework`\n\nPlugin that simplifies `rest_framework` views and other components testing\nby providing following fixtures:\n\n+ `api_rf` - `APIRequestFactory` instance\n+ `api_client` - `APIClient` instance\n",
    'author': 'Bartosz Barwikowski',
    'author_email': 'bartosz.barwikowski@logpass.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://dev.logpass.me',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7.0,<4.0.0',
}


setup(**setup_kwargs)
