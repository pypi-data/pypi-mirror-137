# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['data49']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.10.0,<5.0.0',
 'requests>=2.26.0,<3.0.0',
 'selenium>=3.141.0,<4.0.0',
 'thefuzz[speedup]>=0.19.0,<0.20.0']

setup_kwargs = {
    'name': 'data49',
    'version': '0.2.4',
    'description': 'A gold rush-themed data mining library',
    'long_description': '# data49\n\nA gold rush-themed data mining library\n\nWIP\n\n<!-- It is split into the following sections\n\n - **General utilities** for stuff like functional programming, utility functions, parallel jobs, caching to a file, etc. Wraps `joblib`. Found in the default namespace (`*`)\n  - **Web-related utilities** wrapping web scraping with Beautiful Soup or browser automation with Selenium. Found in the `web` namespace\n  - **Logging** Logging made super easy. Found in the `log` namespace -->\n',
    'author': 'Bryan Hu',
    'author_email': 'bryan.hu.2020@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
