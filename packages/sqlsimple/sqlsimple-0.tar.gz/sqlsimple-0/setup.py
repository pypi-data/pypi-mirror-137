# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sqlsimple']

package_data = \
{'': ['*']}

install_requires = \
['dbutils>=3.0.2,<4.0.0', 'psycopg2>=2.9.3,<3.0.0', 'pystache>=0.6.0,<0.7.0']

setup_kwargs = {
    'name': 'sqlsimple',
    'version': '0',
    'description': 'SQLSimple framework, easy to learn, fast to code, ready for production.',
    'long_description': '**Documentation**:\n    <a href="https://sqlsimple.tiangolo.com" target="_blank">\n        https://sqlsimple.bernardocouto.com\n    </a>\n\n**Source Code**:\n    <a href="https://github.com/bernardocouto/sqlsimple" target="_blank">\n        https://github.com/bernardocouto/sqlsimple\n    </a>\n\n## Installation\n\n```shell\n$ pip install sqlsimple\n```\n\n## License\n\nThis project is licensed under the terms of the [MIT license](https://github.com/bernardocouto/sqlsimple/blob/main/LICENSE).\n',
    'author': 'Bernardo Couto',
    'author_email': 'bernardocouto.py@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/bernardocouto/sqlsimple',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
