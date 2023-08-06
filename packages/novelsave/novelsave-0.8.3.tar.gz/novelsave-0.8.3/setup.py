# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['novelsave',
 'novelsave.client',
 'novelsave.client.bots',
 'novelsave.client.bots.discord',
 'novelsave.client.bots.discord.endpoints',
 'novelsave.client.bots.discord.session',
 'novelsave.client.cli',
 'novelsave.client.cli.controllers',
 'novelsave.client.cli.groups',
 'novelsave.client.cli.helpers',
 'novelsave.core',
 'novelsave.core.dtos',
 'novelsave.core.entities',
 'novelsave.core.entities.novel',
 'novelsave.core.services',
 'novelsave.core.services.cloud',
 'novelsave.core.services.cloud.filehost',
 'novelsave.core.services.config',
 'novelsave.core.services.novel',
 'novelsave.core.services.packagers',
 'novelsave.core.services.source',
 'novelsave.core.services.tools',
 'novelsave.migrations',
 'novelsave.migrations.versions',
 'novelsave.services',
 'novelsave.services.cloud',
 'novelsave.services.cloud.filehost',
 'novelsave.services.config',
 'novelsave.services.novel',
 'novelsave.services.packagers',
 'novelsave.services.source',
 'novelsave.services.tools',
 'novelsave.utils',
 'novelsave.utils.adapters',
 'novelsave.utils.helpers']

package_data = \
{'': ['*'], 'novelsave': ['resources/web/*', 'resources/web/templates/*']}

install_requires = \
['EbookLib>=0.17.1,<0.18.0',
 'Mako>=1.1.5,<2.0.0',
 'SQLAlchemy>=1.4.24,<2.0.0',
 'alembic>=1.7.5,<2.0.0',
 'appdirs>=1.4.4,<2.0.0',
 'beautifulsoup4>=4.10.0,<5.0.0',
 'browser-cookie3>=0.13.0,<0.14.0',
 'click>=8.0.1,<9.0.0',
 'dependency-injector>=4.37.0,<5.0.0',
 'loguru>=0.6.0,<0.7.0',
 'lxml>=4.6.5,<5.0.0',
 'novelsave-sources>=0.3.2,<0.4.0',
 'requests>=2.26.0,<3.0.0',
 'tabulate>=0.8.9,<0.9.0',
 'tqdm>=4.62.3,<5.0.0']

extras_require = \
{'discord': ['nextcord>=2.0.0-alpha.3,<3.0.0']}

entry_points = \
{'console_scripts': ['novelsave = novelsave.client.cli.main:main',
                     'novelsave-discord-bot = '
                     'novelsave.client.bots.discord.main:main']}

setup_kwargs = {
    'name': 'novelsave',
    'version': '0.8.3',
    'description': 'This is a tool to download and convert novels from popular sites to e-books.',
    'long_description': "# NovelSave\n\n![PyPI](https://img.shields.io/pypi/v/novelsave)\n![Python Version](https://img.shields.io/badge/Python-v3.8-blue)\n![Last Commit](https://img.shields.io/github/last-commit/mensch272/novelsave/main)\n![Issues](https://img.shields.io/github/issues/mensch272/novelsave)\n![Pull Requests](https://img.shields.io/github/issues-pr/mensch272/novelsave)\n[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/mensch272/novelsave/main.svg)](https://results.pre-commit.ci/latest/github/mensch272/novelsave/main)\n[![License](https://img.shields.io/github/license/mensch272/novelsave)](LICENSE)\n![Discord](https://img.shields.io/discord/911120379341307904)\n\nThis is a tool to download and convert novels from popular sites to e-books.\n\n> **v0.7.+ is not compatible with previous versions**\n\n## Install\n\n### Local\n\n```bash\npip install novelsave\n```\n\nor\n\n```bash\npip install git+https://github.com/mensch272/novelsave.git\n```\n\n### Chatbots\n\n#### Discord\n\nJoin our server: https://discord.gg/eFgtrKTFt3\n\n##### Environmental Variables\n\nThe default environmental variables are shown below. Modify them to your liking when deploying.\n\n`DISCORD_TOKEN` is required, others are optional.\n\n```shell\nDISCORD_TOKEN=  # Required: discord bot token\nDISCORD_SESSION_TIMEOUT=10 # Minutes\nDISCORD_SESSION_THREADS=5\nDISCORD_SEARCH_LIMIT=20  # Maximum results to show\nDISCORD_SEARCH_DISABLED=no  # Disable search functionality\nDISCORD_EXTERNAL_FILEHOST=none  # options: anonfiles, gofiles, none\n```\n\n#### Heroku Deployment\n\nFill out the following form and set the environmental variables.\n\n[![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy)\n\n## Usage\n\n### Basic\n\nTo download and package the novel in a single line use the following command:\n\n```bash\nnovelsave process <id_or_url>\n```\n\nThe most common commands you'll be using are:\n\n#### `update`\n\nThe command requires the url of the id of the novel as an argument. When the novel has been identified it attempts to update the current novel information in the following steps:\n\n1. Download the novel webpage.\n2. Update the novel information. This includes title, author and pending chapters.\n3. Identify the chapters with no content and download and update them.\n4. Download any assets that require to be downloaded (assets are identified during chapter download).\n\nNote that, if url is provided and the novel does not already exist in the database, a new novel entry will be created.\n\nFor more information, run\n\n```bash\nnovelsave update --help\n```\n\n#### `package`\n\nThe command requires the url of the id of the novel as an argument. When novel is identified compiles the downloaded content into the specified formats.\n\nSpecify a compilation target using the `--target` option. If option is not provided\ncompiles to only epub.\n\nOr you may use `--target-all` to package to all supported formats.\n\n```bash\nnovelsave package <id_or_url> --target epub --target web\n```\n\nSupported compilation targets:\n\n`epub` `html` `mobi` `pdf` `azw3` `text`\n\nFor more information, run\n\n```bash\nnovelsave package --help\n```\n\n#### `process`\n\nThe command requires the url of the id of the novel as an argument. This is a combination of the above two commands, `update` and `package`.\n\nThis is a command of convenience, to update and package in a single command.\n\nFor more information, run\n\n```bash\nnovelsave process --help\n```\n\n### Configurations\n\nUse the following command to show all the current configurations. Default value will be shown\nin case none is set.\n\n```bash\nnovelsave config show\n```\n\nYou may change your configurations using `set` or `reset`. For example:\n\n```bash\nnovelsave config set novel.dir --value ~/mynovels\n```\n\n```bash\nnovelsave config reset novel.dir\n```\n\nAll supported configurations are:\n\n- `novel.dir` - Your desired novel's packaged data (epub, mobi) save location\n\n### More\n\nTo find more information, use option `--help` on groups and commands.\n\n```bash\nnovelsave --help\n```\n\n```bash\nnovelsave novel --help\n```\n\n## Cookies\n\nWant to access authentication protected content, use browser cookies.\n\n### Browser cookies\n\nThis is an optional feature where you may use cookies from your browsers when sending requests.\nThis effectively allows the script to pretend as the browser and thus allowing access to any content\nthe browser would also be able to access.\n\nYou can use this in the following simple steps:\n\n1. Login to your source of choice with your browser of choice (though make sure the browser is supported).\n2. Use option `--browser <browser>` when updating novel (also available in process).\n\n```bash\nnovelsave [update|process] <id_or_url> --browser <browser>\n```\n\n**Supported**\n\n`chrome` `firefox` `chromium` `opera` `edge` `brave`\n\n## Sources\n\nSources have been moved to its own [package](https://github.com/mensch272/novelsave_sources). You can install and upgrade sources using the following command.\n\n```bash\npip install novelsave-sources --upgrade\n```\n\n## Disclaimer\n\nWe are not affiliated, associated, authorized, endorsed by, or in any way officially connected with the any of the [sources](#sources) mentioned above.\n\n## License\n\n[Apache-2.0](https://github.com/mensch272/novelsave/blob/master/LICENSE)\n",
    'author': 'Mensch272',
    'author_email': '47662901+mensch272@users.noreply.github.com',
    'maintainer': 'Mensch272',
    'maintainer_email': '47662901+mensch272@users.noreply.github.com',
    'url': 'https://github.com/mensch272/novelsave',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
