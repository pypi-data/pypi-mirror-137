# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['schemasheets', 'schemasheets.conf', 'schemasheets.utils']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=3.0.3,<4.0.0',
 'bioregistry>=0.4.30,<0.5.0',
 'linkml>=1.1.15,<2.0.0',
 'ontodev-cogs>=0.3.3,<0.4.0']

entry_points = \
{'console_scripts': ['sheets2linkml = schemasheets.schemamaker:convert',
                     'sheets2project = '
                     'schemasheets.sheets_to_project:multigen']}

setup_kwargs = {
    'name': 'schemasheets',
    'version': '0.1.6',
    'description': 'Package to author schemas using spreadsheets',
    'long_description': '# Schemasheets - make datamodels using spreadsheets\n\n<p align="center">\n    <a href="https://github.com/linkml/schemasheets/actions/workflows/main.yml">\n        <img alt="Tests" src="https://github.com/linkml/schemasheets/actions/workflows/main.yml/badge.svg" />\n    </a>\n    <a href="https://pypi.org/project/linkml">\n        <img alt="PyPI" src="https://img.shields.io/pypi/v/linkml" />\n    </a>\n    <a href="https://pypi.org/project/sssom">\n        <img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/sssom" />\n    </a>\n    <a href="https://github.com/linkml/schemasheets/blob/main/LICENSE">\n        <img alt="PyPI - License" src="https://img.shields.io/pypi/l/sssom" />\n    </a>\n    <a href="https://github.com/psf/black">\n        <img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Code style: black">\n    </a>\n</p>\n\nSchemasheets is a framework for managing your schema using\nspreadsheets (Google Sheets, Excel). It works by compiling down to\n[LinkML](https://linkml.io), which can itself be compuled to a variety\nof formalisms.\n\nFor more info, see the [documentation](https://linkml.io/schemasheets)\n',
    'author': 'cmungall',
    'author_email': 'cjm@berkeleybop.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/linkml/schemasheets',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
