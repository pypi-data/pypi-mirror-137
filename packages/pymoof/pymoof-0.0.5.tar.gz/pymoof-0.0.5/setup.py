# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pymoof', 'pymoof.clients', 'pymoof.profiles', 'pymoof.tools', 'pymoof.util']

package_data = \
{'': ['*']}

install_requires = \
['bleak>=0.14.2,<0.15.0',
 'cryptography>=36.0.1,<37.0.0',
 'requests>=2.27.1,<3.0.0']

setup_kwargs = {
    'name': 'pymoof',
    'version': '0.0.5',
    'description': 'Connect to your Vanomof S3/X3 bike',
    'long_description': '# pymoof\n[![ReadTheDocs](https://readthedocs.org/projects/pymoof/badge/?version=latest)](https://pymoof.readthedocs.io/en/latest/) [![PyPI version](https://badge.fury.io/py/pymoof.svg)](https://badge.fury.io/py/pymoof) [![Tests](https://github.com/quantsini/pymoof/actions/workflows/test.yml/badge.svg)](https://github.com/quantsini/pymoof/actions/workflows/test.yml)\n\nConnect to your Vanmoof S3 and X3 through bluetooth.\n\n## Installation\nInstall python 3.7+, then use pip to install pymoof.\n`pip install pymoof`\n\n## Usage\npymoof was tested to work on MacOS 12.1, Ubuntu 20.04.3 LTS, and a Raspberry Pi 3 b+ running Raspberry Pi OS (32-bit) / 2021-10-30.\n```python\nfrom pymoof.clients.sx3 import SX3Client\nimport bleak\n\n...\n\ndevice = ...\nkey = ...\nasync with bleak.BleakClient(device) as bleak_client:\n\tclient = SX3Client(bleak_client, encryption_key)\n\tawait client.authenticate()\n```\nYou must have an instantiated bleak client that is connected to the bike. See `pymoof.tools.discover_bike` to determine which device is your bike and `pymoof.tools.retrieve_encryption_key` to connect to Vanmoof servers to get your encryption key.\n\nSee `example.py` for more info on useage.\n\n## Contributing\nThis project uses [Poetry](https://python-poetry.org/docs/master/#installing-with-the-official-installer) for package and dependency management. It also uses [tox](https://www.tox.wiki/) for test running and pre-commit for running linters.\n',
    'author': 'Henri Bai',
    'author_email': 'quantsini@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/quantsini/pymoof',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
