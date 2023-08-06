# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['win_gpg_agent']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.3,<9.0.0', 'psutil>=5.9.0,<6.0.0']

entry_points = \
{'console_scripts': ['win-gpg-agent = win_gpg_agent:cli']}

setup_kwargs = {
    'name': 'win-gpg-agent',
    'version': '0.1.1',
    'description': 'Utility for tunnelling gpg-agent and ssh-agent from Windows to WSL.',
    'long_description': '# win-gpg-agent\n\nUtility for tunnelling `gpg-agent` and `ssh-agent` from Windows to WSL.\n\nPrimarily used to enable the usage of Yubikeys on WSL.\n\n## Installation\n```\npip install win-gpg-agent\n```\n\n## Usage\n```\n# bash\nwin-gpg-agent export >> ~/.bashrc\n\n# fish\necho "win-gpg-agent export | source" >> ~/.config/fish/config.fish\n```\n\n```\nUsage: win-gpg-agent [OPTIONS] COMMAND [ARGS]...\n\n  Utility for tunnelling gpg-agent and ssh-agent from Windows to WSL.\n\nOptions:\n  --help  Show this message and exit.\n\nCommands:\n  export  Prints SSH_AUTH_SOCK export\n  kill    Kills active tunnels\n  run     Runs tunnel in the foreground\n  start   Starts the daemon\n  status  Prints status information about running tunnels\n  stop    Stops the daemon\n```\n## Credit\nThis work is largely based around previous work from\n- [@Nimamoh](https://github.com/Nimamoh)  \n  [Blog post on WSL2+GPG+Yubikey](https://blog.nimamoh.net/yubi-key-gpg-wsl2-win-gpg-agent/) and [`win-gpg-agent-relay.sh` gist](https://gist.github.com/Nimamoh/e2df2ba0a99ef221d8cca360c931e5e6).\n- [@rupor](https://github.com/rupor-github/win-gpg-agent)  \n  The Windows component to this utility.',
    'author': 'Christian Volkmann',
    'author_email': 'ch.volkmann@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/chvolkmann/win_gpg_agent',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
