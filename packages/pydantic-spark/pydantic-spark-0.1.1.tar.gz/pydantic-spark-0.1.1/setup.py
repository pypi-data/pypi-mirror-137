# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pydantic_spark']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.4.0,<2.0.0']

extras_require = \
{'spark': ['pyspark>=3.1.2,<3.2.0']}

entry_points = \
{'console_scripts': ['pydantic-spark = pydantic_spark.__main__:root_main']}

setup_kwargs = {
    'name': 'pydantic-spark',
    'version': '0.1.1',
    'description': 'Converting pydantic classes to spark schemas',
    'long_description': '[![Python package](https://github.com/godatadriven/pydantic-spark/actions/workflows/python-package.yml/badge.svg)](https://github.com/godatadriven/pydantic-spark/actions/workflows/python-package.yml)\n[![codecov](https://codecov.io/gh/godatadriven/pydantic-spark/branch/main/graph/badge.svg?token=5L08GOERAW)](https://codecov.io/gh/godatadriven/pydantic-spark)\n[![PyPI version](https://badge.fury.io/py/pydantic-spark.svg)](https://badge.fury.io/py/pydantic-spark)\n[![CodeQL](https://github.com/godatadriven/pydantic-spark/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/godatadriven/pydantic-spark/actions/workflows/codeql-analysis.yml)\n\n# pydantic-spark\n\nThis library can convert a pydantic class to a spark schema or generate python code from a spark schema.\n\n### Install\n\n```bash\npip install pydantic-spark\n```\n\n### Pydantic class to spark schema\n\n```python\nimport json\nfrom typing import Optional\n\nfrom pydantic_spark.base import SparkBase\n\nclass TestModel(SparkBase):\n    key1: str\n    key2: int\n    key2: Optional[str]\n\nschema_dict: dict = TestModel.spark_schema()\nprint(json.dumps(schema_dict))\n\n```\n\n### Install for developers\n\n###### Install package\n\n- Requirement: Poetry 1.*\n\n```shell\npoetry install\n```\n\n###### Run unit tests\n```shell\npytest\ncoverage run -m pytest  # with coverage\n# or (depends on your local env) \npoetry run pytest\npoetry run coverage run -m pytest  # with coverage\n```\n\n##### Run linting\n\nThe linting is checked in the github workflow. To fix and review issues run this:\n```shell\nblack .   # Auto fix all issues\nisort .   # Auto fix all issues\npflake .  # Only display issues, fixing is manual\n```\n',
    'author': "Peter van 't Hof'",
    'author_email': 'peter.vanthof@godatadriven.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/godatadriven/pydantic-spark',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0',
}


setup(**setup_kwargs)
