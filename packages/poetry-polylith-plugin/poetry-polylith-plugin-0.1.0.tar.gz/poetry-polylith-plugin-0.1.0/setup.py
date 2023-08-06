# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['poetry_polylith_plugin',
 'poetry_polylith_plugin.commands',
 'poetry_polylith_plugin.components']

package_data = \
{'': ['*']}

install_requires = \
['poetry>=1.2.0a2,<2.0.0', 'tomlkit>=0.7.0,<1.0.0']

entry_points = \
{'poetry.application.plugin': ['poetry-polylith-plugin = '
                               'poetry_polylith_plugin:PolylithPlugin']}

setup_kwargs = {
    'name': 'poetry-polylith-plugin',
    'version': '0.1.0',
    'description': 'A Poetry plugin that aims to simplify working with Polylith monorepos',
    'long_description': '# poetry-polylith-plugin\n\nThis is a Python `Poetry` plugin, adding CLI support for the Polylith architecture.\n\n\n## Polylith?\nFrom the [official docs](https://polylith.gitbook.io/polylith/):\n"... Polylith is a software architecture that applies functional thinking at the system scale.\nIt helps us build simple, maintainable, testable, and scalable backend systems. ..."\n\nThere seems to be an ongoing trend in software development towards using __monorepos__.\n\nThis trend is something especially seen in the __Clojure__ community. Polylith is an architecture, and a tool built for Clojure.\n\n\n__This Poetry Plugin brings Polylith to Python!__\n\n\n## Polylith - a monorepo architecture\nPolylith is using a components-first architecture. Similar to LEGO, components are building blocks.\nA component can be shared across apps, tools, libraries, serverless functions and services. \n\n\n## Usage\nThis plugin depends on the latest version - a preview - of [Poetry](https://python-poetry.org/)\nwith functionality for adding custom Plugins. Have a look at the [official Poetry preview docs](https://python-poetry.org/docs/master/) for how to install it.\n\n### Install Poetry & plugins\nWith the latest `Poetry` version installed, you can add plugins.\n\nAdd the [Multiproject](https://github.com/DavidVujic/poetry-multiproject-plugin) plugin, that will enable the very important __workspace__ support to Poetry.\n``` shell\npoetry plugin add poetry-multiproject-plugin\n```\n\nAdd the Polylith plugin:\n``` shell\npoetry plugin add poetry-polylith-plugin\n```\n\nDone!\n\n### Commands\nCreating a new repo.\n\n``` shell\n# create a directory for your code\nmkdir my-repo-folder\ncd my-repo-folder\ngit init\n\n# This command will create a basic pyproject.toml file.\npoetry init\n\n# This command will create a Polylith workspace, with the basic Polylith folder structure and\n# define a top namespace to be used when creating components and bases.\npoetry poly create workspace --name my_namespace\n```\n\nAdd a component:\n\n``` shell\n# This command will create a component - i.e. a Python package in a namespaced folder.\npoetry poly create component --name my_component\n```\n\nAdd a base:\n\n``` shell\n# This command will create a base - i.e. a Python package in a namespaced folder.\npoetry poly create base --name my_example_aws_lambda\n```\n\nAdd a project:\n\n``` shell\n# This command will create a project - i.e. a pyproject.toml in a project folder. No code in this folder.\npoetry poly create project --name my_example_aws_lambada_project\n```\n\n## Differences between the Clojure & Python implementations\nFirst, this plugin only has the very basic features (yet). Functionality will be added, step by step.\n\nIn the [official docs](https://polylith.gitbook.io/polylith/) - and in the `components` section in particular,\nthere is a `interface.clj` file, used to separate an API from the implementation of a component.\n\nThe Python implementation uses the `__init__.py` to accomplish that.\n\nIn the Python implementation, the `pyproject.toml` is used to define bases and components.\n\nIn particular, the `packages` property is used for that.\n\nThis is the top level `pyproject.toml` used during development.\n``` shell\n packages = [\n    {include = "dev", from = "development/src"},\n    {include = "my_namespace/my_component", from = "components/my_component/src"},\n    {include = "my_namespace/my_example_aws_lambda", from = "bases/my_example_lambda/src"},\n]\n```\n\nWhen creating a project, the project specific `pyproject.toml` will include all the used components and bases.\nNote that the packages are referenced relative to the project. This is enabled by the `Multiproject` plugin.\n``` shell\n packages = [\n    {include = "my_namespace/my_component", from = "../../components/my_component/src"},\n    {include = "my_namespace/my_example_aws_lambda", from = "../../bases/my_example_lambda/src"},\n]\n``` \n',
    'author': 'David Vujic',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/davidvujic/poetry-polylith-plugin',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
