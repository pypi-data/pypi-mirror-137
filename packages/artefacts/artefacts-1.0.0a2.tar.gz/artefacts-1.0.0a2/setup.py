# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['artefacts']

package_data = \
{'': ['*']}

install_requires = \
['dbt-core>=1.0.1,<2.0.0',
 'dbt-postgres>=1.0.1,<2.0.0',
 'pydantic>=1.9.0,<2.0.0',
 'toml>=0.10.2,<0.11.0']

setup_kwargs = {
    'name': 'artefacts',
    'version': '1.0.0a2',
    'description': 'Deserialization for dbt artifacts',
    'long_description': "# artefacts\n\nA deserialization library for dbt artifacts.\n\n### Usage\n\nThe simplest way to use artefacts is by importing the `api`.\n\n```py\n>>> import artefacts.api\n\n```\n\nThe `api` provides convenient methods for interacting with your dbt project's compiled artifacts.\n\n#### `artefacts.api.models()`\n\n```py\n>>> models = artefacts.api.models()\n>>> len(models) > 0\nTrue\n\n```\n\n#### `artefacts.api.tests()`\n\n```py\n>>> tests = artefacts.api.tests()\n>>> len(tests) > 0\nTrue\n\n```\n\n### Development Setup\n\nOpen this repository in a Github Codespace. (Click the green `Code` button in the repository's [Github page](https://github.com/tjwaterman99/artefacts) and select `New Codespace`).\n\n#### Testing\n\n```\npoetry run pytest\n```\n\nBy default, pytest will test against the dbt project located at `DBT_PROJECT_DIR`. To test against a different dbt project, update that environment variable and build the project.\n\n```\nexport DBT_PROJECT_DIR=$PWD/dbt_projects/dbt-starter-project\npoetry run dbt build --project-dir $DBT_PROJECT_DIR\npoetry run pytest\n```",
    'author': 'Tom Waterman',
    'author_email': 'tjwaterman99@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
