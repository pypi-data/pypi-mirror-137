# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['terrible_ideas']
install_requires = \
['fishhook>=0.1.4,<0.2.0', 'spelcheck>=0.3.1,<0.4.0']

setup_kwargs = {
    'name': 'terrible-ideas',
    'version': '0.2.1',
    'description': 'Frequently asked-for missing anti-features',
    'long_description': None,
    'author': 'L3viathan',
    'author_email': 'git@l3vi.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
