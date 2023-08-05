# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['epcpm', 'epcpm.cli', 'epcpm.tests', 'epcpm.tests.cli']

package_data = \
{'': ['*'], 'epcpm.tests': ['project/*', 'sunspec/*']}

install_requires = \
['Jinja2>=3.0.3,<4.0.0',
 'PyQt5==5.13.0',
 'Twisted==21.2.0',
 'attrs==20.2.0',
 'canmatrix==0.9.1',
 'click>=7.0.0,<8.0.0',
 'codecov>=2.1.12,<3.0.0',
 'graham==0.1.11',
 'lxml==4.3.0',
 'openpyxl==2.5.12',
 'pycparser==2.21',
 'pyserial==3.4',
 'pysunspec>=2.1.1,<3.0.0',
 'pytest-cov==2.5.1',
 'pytest-qt==3.2.1',
 'pytest-twisted==1.9',
 'pytest==3.8.2',
 'python-can>=3.3.4,<4.0.0',
 'requests==2.26.0',
 'sunspecdemo>=0.1.9,<0.2.0',
 'toolz==0.9.0',
 'tox==2.8.2',
 'twine==1.13.0',
 'xmldiff==2.2']

entry_points = \
{'console_scripts': ['buildui = buildui:compile_ui',
                     'epcconvertparameters = epcpm.cli.convertepp:cli',
                     'epcexportdocx = epcpm.cli.exportdocx:cli',
                     'epcexportsym = epcpm.cli.exportsym:cli',
                     'epcimportsym = epcpm.cli.importsym:cli',
                     'epcparameterstoc = epcpm.cli.parameterstoc:cli',
                     'epcpm = epcpm.__main__:_entry_point',
                     'epcpmcli = epcpm.cli.main:main']}

setup_kwargs = {
    'name': 'epcpm',
    'version': '2022.1.6',
    'description': '',
    'long_description': None,
    'author': 'Alex Anker',
    'author_email': 'alex.anker@epcpower.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
