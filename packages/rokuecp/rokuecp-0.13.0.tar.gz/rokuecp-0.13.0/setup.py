# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['rokuecp']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.0.0',
 'awesomeversion>=21.10.1',
 'backoff>=1.9.0',
 'cachetools>=4.2.4',
 'xmltodict>=0.12.0',
 'yarl>=1.6.0']

setup_kwargs = {
    'name': 'rokuecp',
    'version': '0.13.0',
    'description': 'Asynchronous Python client for Roku (ECP)',
    'long_description': '# Python: Roku (ECP) Client\n\nAsynchronous Python client for Roku devices using the [External Control Protocol](https://developer.roku.com/docs/developer-program/debugging/external-control-api.md).\n\n## About\n\nThis package allows you to monitor and control Roku devices.\n\n## Installation\n\n```bash\npip install rokuecp\n```\n\n## Usage\n\n```python\nimport asyncio\n\nfrom rokuecp import Roku\n\n\nasync def main():\n    """Show example of connecting to your Roku device."""\n    async with Roku("192.168.1.100") as roku:\n        print(roku)\n\n\nif __name__ == "__main__":\n    loop = asyncio.get_event_loop()\n    loop.run_until_complete(main())\n```\n',
    'author': 'Chris Talkington',
    'author_email': 'chris@talkingtontech.com',
    'maintainer': 'Chris Talkington',
    'maintainer_email': 'chris@talkingtontech.com',
    'url': 'https://github.com/ctalkington/python-rokuecp',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
