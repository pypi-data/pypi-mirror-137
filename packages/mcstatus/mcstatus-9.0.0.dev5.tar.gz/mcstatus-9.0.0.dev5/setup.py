# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'mcstatus'}

packages = \
['mcstatus',
 'mcstatus.protocol',
 'mcstatus.scripts',
 'mcstatus.tests',
 'mcstatus.tests.protocol',
 'protocol',
 'scripts']

package_data = \
{'': ['*']}

install_requires = \
['asyncio-dgram==1.2.0',
 'click>=7.1.2,<9',
 'dnspython==2.1.0',
 'typing-extensions>=4.0.1,<5.0.0']

entry_points = \
{'console_scripts': ['mcstatus = mcstatus.scripts.mcstatus:cli']}

setup_kwargs = {
    'name': 'mcstatus',
    'version': '9.0.0.dev5',
    'description': 'A library to query Minecraft Servers for their status and capabilities.',
    'long_description': '![travis build status](https://img.shields.io/travis/Dinnerbone/mcstatus/master.svg)\n[![current PyPI version](https://img.shields.io/pypi/v/mcstatus.svg)](https://pypi.org/project/mcstatus/)\n![supported python versions](https://img.shields.io/pypi/pyversions/mcstatus.svg)\n[![discord chat](https://img.shields.io/discord/936788458939224094.svg?logo=Discord)](https://discord.gg/C2wX7zduxC)\n\nmcstatus\n========\n\n`mcstatus` provides an easy way to query Minecraft servers for any information they can expose.\nIt provides three modes of access (`query`, `status` and `ping`), the differences of which are listed below in usage.\n\nUsage\n-----\n\nJava Edition\n```python\nfrom mcstatus import MinecraftServer\n\n# If you know the host and port, you may skip this and use MinecraftServer("example.org", 1234)\nserver = MinecraftServer.lookup("example.org:1234")\n\n# \'status\' is supported by all Minecraft servers that are version 1.7 or higher.\nstatus = server.status()\nprint(f"The server has {status.players.online} players and replied in {status.latency} ms")\n\n# \'ping\' is supported by all Minecraft servers that are version 1.7 or higher.\n# It is included in a \'status\' call, but is exposed separate if you do not require the additional info.\nlatency = server.ping()\nprint(f"The server replied in {latency} ms")\n\n# \'query\' has to be enabled in a servers\' server.properties file.\n# It may give more information than a ping, such as a full player list or mod information.\nquery = server.query()\nprint(f"The server has the following players online: {\', \'.join(query.players.names)}")\n```\n\nBedrock Edition\n```python\nfrom mcstatus import MinecraftBedrockServer\n\n# If you know the host and port, you may skip this and use MinecraftBedrockServer("example.org", 19132)\nserver = MinecraftBedrockServer.lookup("example.org:19132")\n\n# \'status\' is the only feature that is supported by Bedrock at this time.\n# In this case status includes players_online, latency, motd, map, gamemode, and players_max. (ex: status.gamemode)\nstatus = server.status()\nprint(f"The server has {status.players_online} players online and replied in {status.latency} ms")\n```\n\nCommand Line Interface\n```\n$ mcstatus\nUsage: mcstatus [OPTIONS] ADDRESS COMMAND [ARGS]...\n\n  mcstatus provides an easy way to query Minecraft servers for any\n  information they can expose. It provides three modes of access: query,\n  status, and ping.\n\n  Examples:\n\n  $ mcstatus example.org ping\n  21.120ms\n\n  $ mcstatus example.org:1234 ping\n  159.903ms\n\n  $ mcstatus example.org status\n  version: v1.8.8 (protocol 47)\n  description: "A Minecraft Server"\n  players: 1/20 [\'Dinnerbone (61699b2e-d327-4a01-9f1e-0ea8c3f06bc6)\']\n\n  $ mcstatus example.org query\n  host: 93.148.216.34:25565\n  software: v1.8.8 vanilla\n  plugins: []\n  motd: "A Minecraft Server"\n  players: 1/20 [\'Dinnerbone (61699b2e-d327-4a01-9f1e-0ea8c3f06bc6)\']\n\nOptions:\n  -h, --help  Show this message and exit.\n\nCommands:\n  json    combination of several other commands with json formatting\n  ping    prints server latency\n  query   detailed server information\n  status  basic server information\n```\n\nInstallation\n------------\n\nmcstatus is available on pypi, and can be installed trivially with:\n\n```bash\npython3 -m pip install mcstatus\n```\n\nAlternatively, just clone this repo!\n\nLicense\n-------\n\nmcstatus is licensed under Apache 2.0.\n',
    'author': 'Nathan Adams',
    'author_email': 'dinnerbone@dinnerbone.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Dinnerbone/mcstatus',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
