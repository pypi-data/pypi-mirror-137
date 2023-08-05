# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lwc_common', 'lwc_common.common', 'lwc_common.lwc']

package_data = \
{'': ['*']}

install_requires = \
['google-cloud-storage>=2.1.0,<3.0.0',
 'msedge-selenium-tools>=3.141.3,<4.0.0',
 'requests>=2.27.1,<3.0.0']

setup_kwargs = {
    'name': 'lwc-common',
    'version': '0.1.2',
    'description': '',
    'long_description': None,
    'author': 'AminuIsrael',
    'author_email': 'israel.aminu@data2bots.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
