# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['poetry_githooks']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.3,<9.0.0', 'toml>=0.10.2,<0.11.0']

entry_points = \
{'console_scripts': ['githooks = poetry_githooks:cli']}

setup_kwargs = {
    'name': 'poetry-githooks',
    'version': '2.0.0',
    'description': 'Simple git hooks with poetry',
    'long_description': '# poetry-githooks\n\n## Install\n\nThis repository is made to work with [poetry](https://python-poetry.org/). Assuming you have a working `poetry` setup, run\n\n```\npoetry add -D poetry-githooks\n```\n\n## Install\n\nCreate a `tool.githooks` section in your `pyproject.toml` file and define your git hooks, for example\n\n```\n[tool.githooks]\npre-commit = "black ."\n```\n\nthen run\n\n```\npoetry run githooks setup\n```\n\nThat\'s it :tada: your hooks will be ran using `poetry` when expected\n\n**IMPORTANT** You need to rerun `poetry run githooks setup` everytime you change `[tool.githooks]`\n',
    'author': 'Thomas Thiebaud',
    'author_email': 'thiebaud.tom@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/thomasthiebaud/poetry-githooks',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2,<4.0',
}


setup(**setup_kwargs)
