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
    'version': '0.0.4',
    'description': 'Connect to your Vanomof S3/X3 bike',
    'long_description': '# pymoof\nConnect to your Vanmoof S3 and X3 through bluetooth.\n\n## Installation\nInstall python 3.6+, then use pip to install pymoof.\n`pip install pymoof`\n\n## Usage\n```python\nfrom pymoof.clients.sx3 import SX3Client\n\nclient = SX3Client(bleak_client, encryption_key)\nclient.authenticate()\n```\nYou must have an instantiated bleak client that is connected to the bike. See `pymoof.tools.discover_bike` to determine which device is your bike and `pymoof.tools.retrieve_encryption_key` to connect to Vanmoof servers to get your encryption key.\n\nSee `example.py` for more info on useage.\n\n## Contributing\nThis project uses Poetry for package and dependency management. It also uses tox for test running and pre-commit for running linters.\n',
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
