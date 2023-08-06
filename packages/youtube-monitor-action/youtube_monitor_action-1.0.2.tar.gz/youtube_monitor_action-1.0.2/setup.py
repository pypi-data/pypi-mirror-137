# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['youtube_monitor_action']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.4.1,<6.0.0',
 'importlib-metadata>=4.8.1,<5.0.0',
 'requests>=2.26.0,<3.0.0',
 'xmltodict>=0.12.0,<0.13.0']

entry_points = \
{'console_scripts': ['youtube-monitor-action = '
                     'youtube_monitor_action.__main__:main']}

setup_kwargs = {
    'name': 'youtube-monitor-action',
    'version': '1.0.2',
    'description': 'Monitor for new video on YouTube Channel',
    'long_description': '# youtube_monitor_action\nA utility to perform an action after videos are live on YouTube for a given channel.\n\nThis module provides the script `youtube-monitor-action`\n```\nusage: youtube-monitor-action [-h] [-n N] [--channel CHANNEL] [--store-config]\n                              [--hibernate] [--open-in-browser] [--verbose]\n                              [--quiet] [--version] [--log-file LOG_FILE]\n\noptional arguments:\n  -h, --help           show this help message and exit\n  -n N                 The number of new videos to watch for\n  --channel CHANNEL    (Optional) The channel id to monitor (default: load\n                       from config.yaml)\n  --store-config       Store channel and other settings in config and exit\n\nActions:\n  --hibernate          Hibernate computer once condition is met\n  --open-in-browser    Open new videos in browser\n\ndebug:\n  --verbose, -v        increase verbosity (may be repeated)\n  --quiet, -q          decrease verbosity (may be repeated)\n  --version, -V        print version and exit\n\nlogging:\n  --log-file LOG_FILE  File to log to\n```\n',
    'author': 'mshafer1',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mshafer1/youtube_monitor_action',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
