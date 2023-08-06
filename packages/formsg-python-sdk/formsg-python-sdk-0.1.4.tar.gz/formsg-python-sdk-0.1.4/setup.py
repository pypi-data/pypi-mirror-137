# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['formsg', 'formsg.schemas', 'formsg.util']

package_data = \
{'': ['*']}

install_requires = \
['PyNaCl>=1.5.0,<2.0.0', 'pytest>=6.2.5,<7.0.0', 'requests>=2.27.1,<3.0.0']

setup_kwargs = {
    'name': 'formsg-python-sdk',
    'version': '0.1.4',
    'description': 'Python SDK for FormSG',
    'long_description': None,
    'author': 'Chin Ying',
    'author_email': 'chinying@open.gov.sg',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
