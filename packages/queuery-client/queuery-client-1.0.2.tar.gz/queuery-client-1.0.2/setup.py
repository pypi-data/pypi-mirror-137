# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['queuery_client']

package_data = \
{'': ['*']}

install_requires = \
['python-dateutil>=2.8.2,<3.0.0', 'requests>=2.25.1,<3.0.0']

extras_require = \
{'pandas': ['pandas>=1.2.3,<2.0.0']}

setup_kwargs = {
    'name': 'queuery-client',
    'version': '1.0.2',
    'description': 'Queuery Redshift HTTP API Client for Python',
    'long_description': '# queuery_client_python\n\nQueuery Redshift HTTP API Client for Python\n\n## Installation\n\n`pip install queuery-client`\n\n## Usage\n\n### Prerequisites\n\nSet the following envronment variables to connect Queuery server:\n\n- `QUEUERY_TOKEN`: Specify Queuery access token\n- `QUEUERY_TOKEN_SECRET`:  Specify Queuery secret access token\n- `QUEUERY_ENDPOINT`: Specify a Queuery endpoint URL via environment variables if you don\'t set the `endpoint` argument of `QueueryClient` in you code\n\n### Basic Usage\n\n```python\nfrom queuery_client import QueueryClient\n\nclient = QueueryClient(endpoint="https://queuery.example.com")\nresponse = client.run("select column_a, column_b from the_great_table")\n\n# (a) iterate `response` naively\nfor elems in response:\n    print(response)\n\n# (b) invoke `read()` to fetch all records\nprint(response.read())\n\n# (c) invoke `read()` with `use_pandas=True` (returns `pandas.DataFrame`)\nprint(response.read(use_pandas=True))\n```\n\n### Type Cast\n\nBy default, `QueueryClient` returns all values as `str` regardless of their definitions on Redshift.\nYou can use the `enable_cast` option to automatically convert types of the returned values into appropreate ones based on their definitions.\n\n```python\nfrom queuery_client import QueueryClient\n\nclient = QueueryClient(\n    endpoint="https://queuery.example.com",\n    enable_cast=True,   # Cast types of the returned values automatically!\n)\n\nsql = "select 1, 1.0, \'hoge\', true, date \'2021-01-01\', timestamp \'2021-01-01\', null"\nresponse = client.run(sql)\nresponse.read() # => [[1, 1.0, \'hoge\', True, datetime.date(2021, 1, 1), datetime.datetime(2021, 1, 1, 0, 0), None]]\n```\n',
    'author': 'altescy',
    'author_email': 'yasuhiro-yamaguchi@cookpad.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/bricolages/queuery_client_python',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8.0,<4.0.0',
}


setup(**setup_kwargs)
