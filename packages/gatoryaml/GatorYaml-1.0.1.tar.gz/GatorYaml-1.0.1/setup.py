# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gatoryaml']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'gatoryaml',
    'version': '1.0.1',
    'description': 'Custom YAML-like generator for GatorGrader config files.',
    'long_description': '# GatorYAML\n\n![GatorYAML Logo](https://i.imgur.com/E4masCO.png)\n\nCustom YAML-like generator for GatorGrader config files.\n',
    'author': 'Danny Ullrich',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/ullrichd21/GatorYaml',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
