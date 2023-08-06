# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flycs_sdk', 'tests']

package_data = \
{'': ['*']}

install_requires = \
['chardet>=4.0.0,<5.0.0',
 'requirements-parser>=0.2.0,<0.3.0',
 'ruamel.yaml>=0.16.12,<0.17.0',
 'semver>=2.13.0,<3.0.0',
 'urllib3>=1.26.5,<2.0.0']

setup_kwargs = {
    'name': 'flycs-sdk',
    'version': '0.11.0',
    'description': 'Top-level package for Flycs SDK.',
    'long_description': '=========\nFlycs SDK\n=========\n\n\n.. image:: https://img.shields.io/pypi/v/flycs_sdk.svg\n        :target: https://pypi.python.org/pypi/flycs_sdk\n\n.. image:: https://github.com/Fourcast/flycs_sdk/workflows/Test%20package/badge.svg\n        :target: https://github.com/Fourcast/flycs_sdk/actions?query=workflow%3A%22Test+package%22\n        :alt: Test status\n\n.. image:: https://readthedocs.org/projects/flycs-sdk/badge/?version=stable\n        :target: https://flycs-sdk.readthedocs.io/en/stable/?badge=stable\n        :alt: Documentation Status\n\n\n.. image:: https://pyup.io/repos/github/Fourcast/flycs_sdk/shield.svg\n     :target: https://pyup.io/repos/github/Fourcast/flycs_sdk/\n     :alt: Updates\n\n\n\nFlycs SDK contains the Python SDK to interact with the Flycs data framework.\n\n\n* Free software: MIT\n* Documentation: https://flycs-sdk.readthedocs.io.\n\n\nFeatures\n--------\n\n* Allows you to create the data objects needed to interact with Flycs.\n\nCredits\n-------\n\nThis package was created with Cookiecutter_ and the `briggySmalls/cookiecutter-pypackage`_ project template.\n\n.. _Cookiecutter: https://github.com/audreyr/cookiecutter\n.. _`briggySmalls/cookiecutter-pypackage`: https://github.com/briggySmalls/cookiecutter-pypackage\n',
    'author': 'Tristan Van Thielen',
    'author_email': 'tristan.van.thielen@devoteam.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Fourcast/flycs_sdk',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.2,<3.11',
}


setup(**setup_kwargs)
