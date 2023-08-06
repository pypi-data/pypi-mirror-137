# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['getthenews', 'getthenews.utils']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.10.0,<5.0.0',
 'fake-headers>=1.0.2,<2.0.0',
 'requests>=2.27.1,<3.0.0',
 'rich>=11.1.0,<12.0.0']

entry_points = \
{'console_scripts': ['getthenews = getthenews.main:argument']}

setup_kwargs = {
    'name': 'getthenews',
    'version': '0.1.1',
    'description': 'Get the latest news using command line.',
    'long_description': '\n## Project Introduction\n\nA small library to search for news using command line.\n\n\n## Installation\n\n```python\npip install getthenews\n```\n\n### Usage\n\n\n```python\ngetthenews --help\n```\n\n> --help can be used to get the info about commands we can use.\n\n#### Examples\n\n```python\ngetthenews --query ai --lang en --size 10\n\n```\n> gets 10 news(english) related to artificial intelligence.\n\n\n',
    'author': 'xettrisomeman',
    'author_email': 'webizmoxx@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
