# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cygnods']

package_data = \
{'': ['*']}

install_requires = \
['configparser>=5.2.0', 'numpy>=1.16.5', 'opencv-python>=4.4.0']

setup_kwargs = {
    'name': 'cygnods',
    'version': '0.1.1',
    'description': 'Small library to handle most frequent CYGNO dataset operations with python',
    'long_description': '# cygnods\nSmall library to handle most frequent CYGNO dataset operations with python\n',
    'author': 'Gustavo Viera López',
    'author_email': 'gvieralopez@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/CYGNO-ML/cygnods',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
