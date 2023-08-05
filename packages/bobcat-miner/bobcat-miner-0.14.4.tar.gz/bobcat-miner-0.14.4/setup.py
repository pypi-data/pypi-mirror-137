# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['bobcat_miner']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.1,<4.0.0',
 'backoff>=1.11.1,<2.0.0',
 'beautifulsoup4>=4.10.0,<5.0.0',
 'click>=8.0.3,<9.0.0',
 'discord-lumberjack>=1.0.4,<2.0.0',
 'filelock>=3.4.2,<4.0.0',
 'requests>=2.27.0,<3.0.0']

entry_points = \
{'console_scripts': ['bobcat = bobcat_miner.cli:cli']}

setup_kwargs = {
    'name': 'bobcat-miner',
    'version': '0.14.4',
    'description': "A command line tool used to automate the Bobcat miner. This project also offers a robust python SDK's for interacting with the Bobcat miner.",
    'long_description': '[![PyPI](https://img.shields.io/pypi/v/bobcat_miner.svg)](https://pypi.org/project/bobcat-miner/)\n[![Dockerhub](https://img.shields.io/docker/v/aidanmelen/bobcat?color=blue&label=docker%20build)](https://hub.docker.com/r/aidanmelen/bobcat)\n[![Release](https://github.com/aidanmelen/bobcat-miner-python/actions/workflows/release.yaml/badge.svg)](https://github.com/aidanmelen/bobcat-miner-python/actions/workflows/release.yaml)\n[![Tests](https://github.com/aidanmelen/bobcat-miner-python/actions/workflows/tests.yaml/badge.svg)](https://github.com/aidanmelen/bobcat-miner-python/actions/workflows/tests.yaml)\n[![Lint](https://github.com/aidanmelen/bobcat-miner-python/actions/workflows/lint.yaml/badge.svg)](https://github.com/aidanmelen/bobcat-miner-python/actions/workflows/lint.yaml)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\n\n# bobcat miner python\n\nA command line tool used to automate the Bobcat miner. This project also offers a robust python SDK\'s for interacting with the Bobcat miner.\n\n## Install\n\n```bash\n$ pipx install bobcat-miner\n```\n\nPlease see this [guide](https://packaging.python.org/en/latest/guides/installing-stand-alone-command-line-tools/) for more information about installing stand alone command line tools with [pipx](https://pypa.github.io/pipx/).\n\n## Quick Start\n\nThe `bobcat autopilot` command will automatically diagnose and repair the Bobcat miner!\n\n```bash\n$ bobcat autopilot\n✅ Sync Status: Synced (gap:-1) ✨\n✅ Relay Status: Not Relayed ✨\n✅ Network Status: Good 📶\n✅ Temperature Status: Good (38°C) ☀️\n```\n\nor run with the offical Docker image\n\n```bash\n$ docker run --rm -it aidanmelen/bobcat autopilot\n```\n\nRun `bobcat --help` to learn about the available commands and options.\n\n## Finding your Bobcat\n\nBy default, the Bobcat Autopilot will search the common `192.168.0.0/24` and `10.0.0.0/24` local networks to find the Bobcat miner.\n\n### Find Bobcat by Animal Name\n\nThis will connect to the Bobcat on your network that matches the animal name.\n\n```bash\n$ bobcat --animal "Fancy Awesome Bobcat" -C DEBUG autopilot\n🐛 Connected to Bobcat: 192.168.0.10\n🐛 Refresh: Miner Data\n🐛 Verified Bobcat Animal: fancy-awesome-bobcat\n🐛 The Bobcat Autopilot is starting 🚀 🚀 🚀\n```\n\n### Specify the Hostname / IP Address\n\nOtherwise, you can follow these [instructions](https://bobcatminer.zendesk.com/hc/en-us/articles/4412905935131-How-to-Access-the-Diagnoser) to find your Bobcats\'s ip address and specify it with:\n\n```bash\n$ bobcat --hostname 192.168.0.10 -C DEBUG autopilot\n🐛 Connected to Bobcat: 192.168.0.10\n🐛 The Bobcat Autopilot is starting 🚀 🚀 🚀\n```\n\n## Monitoring with Discord\n\nMonitor your Bobcat remotely by sending events to a Discord channel by specifying a [webhook URL](https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks). No need for VPN or SSH agent setup!\n\n```bash\n$ bobcat --discord-webhook-url https://discord.com/api/webhooks/xxx autopilot\n✅ Sync Status: Synced (gap:0) ✨\n⚠️ Relay Status: Relayed\n✅ Network Status: Good 📶\n❌ Temperature Status: Hot (78°C) 🌋\n```\n\nBy default, all events `WARNING` or higher (i.e. `ERROR` and `CRITICAL`) will be sent to the Discord channel. This can be configured to include `DEBUG` and `INFO` events as well.\n\n<!-- <img src="https://raw.githubusercontent.com/aidanmelen/bobcat-miner-python/main/assets/bobcat-autopilot-discord-app.png" alt="drawing" style="width:500px;"/> -->\n<img src="https://raw.githubusercontent.com/aidanmelen/bobcat-miner-python/main/assets/bobcat-autopilot-discord-app.png" alt="drawing" width="300"/>\n\n### Dry Run\n\nThis example is admittedly contrived, but it demonstrates how the `--dry-run` option can be used show what actions would normally be performed against the bobcat without actually running them.\n\n```bash\n$ bobcat --dry-run reboot\nDo you want to reboot the Bobcat? [y/N]: y\n⚠️ Dry run is enabled: Reboot Skipped\n```\n\n## Bobcat SDK\n\nPlease see [docs/bobcat_sdk.md](https://raw.githubusercontent.com/aidanmelen/bobcat-miner-python/main/docs/bobcat_sdk.md) for more information.\n\n\n## Contributions\n\nPlease see [docs/contributions.md](https://raw.githubusercontent.com/aidanmelen/bobcat-miner-python/main/docs/contributions.md) for more information.\n\n## Troubleshooting\n\nPlease see [No Witness\'s Troubleshooting Guide](https://www.nowitness.org/troubleshooting/) for more information.\n\n## Donations\n\nDonations are welcome and appreciated! :gift:\n\n[![HNT: 14HmckNU4WHDDtGH29FMqVENzZAYh5a9XRiLfY2AN6ghfHMvAuR](https://raw.githubusercontent.com/aidanmelen/bobcat-miner-python/main/assets/wallet.jpg)](https://explorer-v1.helium.com/accounts/14HmckNU4WHDDtGH29FMqVENzZAYh5a9XRiLfY2AN6ghfHMvAuR)\n\nHNT: [14HmckNU4WHDDtGH29FMqVENzZAYh5a9XRiLfY2AN6ghfHMvAuR](https://explorer-v1.helium.com/accounts/14HmckNU4WHDDtGH29FMqVENzZAYh5a9XRiLfY2AN6ghfHMvAuR)\n',
    'author': 'Aidan Melen',
    'author_email': 'aidanmelen@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/aidanmelen/bobcat-miner-python',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
