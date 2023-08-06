# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['filesystem', 'filesystem.fmt']

package_data = \
{'': ['*']}

install_requires = \
['PyExcelerate',
 'PyYAML',
 'XlsxWriter',
 'chardet',
 'h5py',
 'iniconfig',
 'openpyxl',
 'toml',
 'untangle',
 'xlrd==1.2.0',
 'xmltodict']

setup_kwargs = {
    'name': 'filesystem-python',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'kagemeka',
    'author_email': 'kagemeka1@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
