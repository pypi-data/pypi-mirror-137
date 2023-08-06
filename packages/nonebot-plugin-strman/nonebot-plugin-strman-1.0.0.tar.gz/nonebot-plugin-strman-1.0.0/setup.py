# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_strman']

package_data = \
{'': ['*']}

install_requires = \
['nonebot2>=2.0.0-beta.1,<3.0.0']

setup_kwargs = {
    'name': 'nonebot-plugin-strman',
    'version': '1.0.0',
    'description': 'A string management tool for NoneBot 2',
    'long_description': 'None',
    'author': 'Satoshi Jek',
    'author_email': 'jks15satoshi@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
