# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lwc_common', 'lwc_common.lwc', 'lwc_common.wrappers']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy>=1.4.31,<2.0.0',
 'google-cloud-storage>=2.1.0,<3.0.0',
 'msedge-selenium-tools>=3.141.4,<4.0.0',
 'pg8000>=1.23.0,<2.0.0',
 'requests>=2.27.1,<3.0.0']

setup_kwargs = {
    'name': 'lwc-common',
    'version': '0.3.0rc2',
    'description': '',
    'long_description': '# LinkedIn Web Crawler Common Library\n\n[//]: # ([![Tests]&#40;https://github.com/data2bots-internal/data2bots-internship-linkedincrawler/actions/workflows/tests.yml/badge.svg?branch=develop&#41;]&#40;https://github.com/data2bots-internal/data2bots-internship-linkedincrawler/actions/workflows/tests.yml&#41;)\n<a href="https://data2bots.com/"><img src="https://res.cloudinary.com/kolaisaac10/image/upload/v1632051038/samples/Companies/data2bots_mjqhxe.png" alt="Data2Bots" width="120" height="45" /> </a>\n\n*Data2Bots...Human capital is the greatest asset*\n\n---\n\n- Inputs a search parameter on Google (e.g. "Data Engineer")\n- Logins in to LinkedIn (www.linkedin.com/login)\n- Crawls individual LinkedIn URLs based on the search result\n\n\n### Special thanks to the Data Engineering Team at Data2Bots\n',
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
