# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sirius', 'sirius.core', 'sirius.routing']

package_data = \
{'': ['*']}

install_requires = \
['tomli>=2.0.0,<3.0.0', 'uvicorn[standard]>=0.17.1,<0.18.0']

entry_points = \
{'console_scripts': ['sirius = sirius.__main__:main']}

setup_kwargs = {
    'name': 'sirius-api',
    'version': '0.1.2',
    'description': 'Create APIs that shine like a star',
    'long_description': None,
    'author': 'Vivaan Verma',
    'author_email': 'hello@vivaanverma.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
