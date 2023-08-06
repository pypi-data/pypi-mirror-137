# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['cleanurl']

package_data = \
{'': ['*']}

install_requires = \
['urllib3>=1.26.8,<2.0.0']

setup_kwargs = {
    'name': 'cleanurl',
    'version': '0.1.0',
    'description': 'Removes clutter from URLs and returns a canonicalized version',
    'long_description': None,
    'author': 'Alexandru Cojocaru',
    'author_email': 'hi@xojoc.pw',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
