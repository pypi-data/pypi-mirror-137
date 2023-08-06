# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

modules = \
['cleanurl']
setup_kwargs = {
    'name': 'cleanurl',
    'version': '0.1.1',
    'description': 'Removes clutter from URLs and returns a canonicalized version',
    'long_description': '# cleanurl\nRemoves clutter from URLs and returns a canonicalized version\n',
    'author': 'Alexandru Cojocaru',
    'author_email': 'hi@xojoc.pw',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/xojoc/cleanurl',
    'package_dir': package_dir,
    'py_modules': modules,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
