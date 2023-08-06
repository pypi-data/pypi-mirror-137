# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['poetry_multiproject_plugin',
 'poetry_multiproject_plugin.commands',
 'poetry_multiproject_plugin.commands.build',
 'poetry_multiproject_plugin.overrides',
 'poetry_multiproject_plugin.workspace']

package_data = \
{'': ['*']}

install_requires = \
['poetry>=1.2.0a2,<2.0.0']

entry_points = \
{'poetry.application.plugin': ['poetry-multiproject-plugin = '
                               'poetry_multiproject_plugin:MultiProjectPlugin']}

setup_kwargs = {
    'name': 'poetry-multiproject-plugin',
    'version': '0.3.3',
    'description': 'A Poetry plugin that aims to simplify package & dependency management for projects in Monorepos.',
    'long_description': '# Poetry Multiproject Plugin\n\nThis is a Python `Poetry` plugin, adding commands with support for including packages outside of a project root.\n\nThis is achieved by setting the workspace (or commonly the repo) folder as the root folder.\nAlso, the plugin makes it possible specify a project specific `pyproject.toml` file,\nuseful when running commands from the workspace root.\n\nExample usage:\nrunning the command from the workspace root folder\n\n``` shell\npoetry build-project -t path/to/pyproject.toml\n```\n\nOptionally, run the command from the same folder as the actual project specific TOML file:\n\n``` shell\npoetry build-project\n```\n\n## Workspace?\nA workspace is a place for code and projects. Within the workspace, code can be shared. A workspace is usually at the root\nof your repository. To enable your Python project as a workspace, just add an empty `workspace.toml` file at the top.\n\n``` shell\ntouch workspace.toml\n```\n\nThe plugin will look for the `workspace.toml` file to determine the workspace root.\n\n\n## Why workspaces?\nBeing able to specify package includes outside of a project root is especially\nuseful when structuring code in a Monorepo, where projects can share components.\n\nWhen the plugin is installed, there is a new command available: `build-project`.\n\n## How is it different from the "poetry build" command?\nPoetry doesn\'t seem allow to reference code that is outside of the __project__ root.\n\nSomething like this will cause the build to fail:\n\n``` shell\n# this will fail using the default poetry build command\n\npackages = [\n    { include = "my_namespace/my_package" from = "../../my_shared_folder" }\n]\n```\n\nBy explicitly setting a workspace root, it is possible to reference outside components like this:\n\n``` shell\n# this will work, when using the build-project command.\n\n# Note the structure of the shared folder: namespace/package/*.py\n\npackages = [\n    { include = "my_namespace/my_package" from = "../../my_shared_folder" }\n]\n```\n\nSimplified example of a monorepo structure:\n\n``` shell\nprojects/\n  my_app/\n    pyproject.toml (including a shared package)\n\n  my_service/\n    pyproject.toml (including other shared packages)\n\nshared/\n  my_namespace/\n    my_package/\n      __init__.py\n      code.py\n\n    my_other_package/\n      __init__.py\n      code.py\n\nworkspace.toml (a file that tells the plugin where to find the workspace root)\n```\n\n## Using the preview of Poetry\nThis plugin depends on a preview of [Poetry](https://python-poetry.org/) with functionality for adding custom Plugins.\nHave a look at the [official Poetry preview docs](https://python-poetry.org/docs/master/) for how to install it.\n\nInstall the plugin according to the [official Poetry docs](https://python-poetry.org/docs/master/cli/#plugin).\n\nWhen installed, there will be a new command available: `build-project`.\n\n\n## Modifying the Poetry internals\nSetting the workspace root is done by altering the internal properties of the Poetry objects.\nThis is (naturally) a risk, an update of the Poetry tool could break the functionality of the plugin.\n\nA long-term goal is to [make a Pull Request](https://github.com/python-poetry/poetry-core/pull/273) to the Poetry repository,\nmaking this kind of functionality available in there. This plugin would no longer be necessary if the pull request is accepted and merged.\n\n## What\'s next? Any other commands?\nStarting with the `build-project` command, and ready to add more custom commands\nif any of the existing ones are relevant to override when using a project specific TOML file.\n\n',
    'author': 'David Vujic',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/davidvujic/poetry-multiproject-plugin',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
