# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aiohtml2pdf']

package_data = \
{'': ['*']}

install_requires = \
['pyppeteer>=1.0.2,<2.0.0']

setup_kwargs = {
    'name': 'aiohtml2pdf',
    'version': '0.1.0a0',
    'description': '',
    'long_description': None,
    'author': 'Albert Khachatryan',
    'author_email': 'ht.albert2606@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
