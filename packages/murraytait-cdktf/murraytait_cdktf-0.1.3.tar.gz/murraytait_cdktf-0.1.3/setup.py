# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['murraytait_cdktf', 'murraytait_cdktf.tests']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.20.31,<2.0.0',
 'cdktf-cdktf-provider-aws>=4.0.2,<5.0.0',
 'cdktf>=0.8.6,<0.9.0',
 'constructs>=10.0.29,<11.0.0',
 'pytest-mock>=3.6.1,<4.0.0']

setup_kwargs = {
    'name': 'murraytait-cdktf',
    'version': '0.1.3',
    'description': '',
    'long_description': None,
    'author': 'Murray Tait',
    'author_email': '6074789+deathtumble@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
