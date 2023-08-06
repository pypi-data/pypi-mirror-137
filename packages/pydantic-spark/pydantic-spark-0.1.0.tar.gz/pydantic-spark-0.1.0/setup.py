# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pydantic_spark']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.0.0']

entry_points = \
{'console_scripts': ['pydantic-spark = pydantic_spark.__main__:root_main']}

setup_kwargs = {
    'name': 'pydantic-spark',
    'version': '0.1.0',
    'description': 'Converting pydantic classes to spark schemas',
    'long_description': '',
    'author': "Peter van 't Hof'",
    'author_email': 'peter.vanthof@godatadriven.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/godatadriven/pydantic-spark',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0',
}


setup(**setup_kwargs)
