# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['texipy']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'texipy',
    'version': '0.1.1',
    'description': 'Python for LaTeX',
    'long_description': '"# TeXiPy" \n',
    'author': 'Praveen Kulkarni',
    'author_email': 'praveenneuron@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
