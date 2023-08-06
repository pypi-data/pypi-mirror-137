# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['stoplight']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.27.1,<3.0.0',
 'rich>=11.1.0,<12.0.0',
 'toml>=0.10.2,<0.11.0',
 'typer[all]>=0.4.0,<0.5.0',
 'types-requests>=2.27.8,<3.0.0',
 'types-toml>=0.10.3,<0.11.0']

entry_points = \
{'console_scripts': ['stoplight = stoplight.run:app']}

setup_kwargs = {
    'name': 'pystoplight',
    'version': '1.0.0',
    'description': 'A tool that enables educators to easily control push access to GitHub Classroom assignment repositories.',
    'long_description': '# Stoplight\n\n[![Lint and Test](https://github.com/mariakimheinert/stoplight/actions/workflows/main.yml/badge.svg?branch=main)](https://github.com/mariakimheinert/stoplight/actions/workflows/main.yml)\n[![PyPI](https://img.shields.io/pypi/v/pystoplight)](https://pypi.org/project/pystoplight)\n![PyPI - Python Versions](https://img.shields.io/pypi/pyversions/pystoplight)\n[![PyPI - Downloads](https://img.shields.io/pypi/dm/pystoplight)](https://pypi.org/project/pystoplight/#files)\n[![License](https://img.shields.io/github/license/mariakimheinert/stoplight)](https://github.com/mariakimheinert/stoplight/blob/master/LICENSE)\n\n`stoplight` is a tool that enables educators to easily control push access to GitHub Classroom assignment repositories.\n\nPlease note that, as of now, `stoplight` only supports at most 100 student repositories per GitHub Classroom assignment.\n\n## Installation\n\nPython 3.10 required. [`pipx`](https://pypa.github.io/pipx/) recommended.\n\n```console\npipx install pystoplight\n```\n\n## Usage\n\n### Authentication\n\nRequires a [GitHub personal access token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token).\n\nOnce created, place in your `.stoplightrc` file, which you can store either in the directory where you execute `stoplight` or in your home directory.\n\n```toml\ntoken = "<TOKEN>"\n```\n\nOr, you can pass it in as the value of the `--token` option.\n\n```console\nstoplight red --token <TOKEN>\n```\n\n### Commands\n\n#### `stoplight status`\n\nTo check the permissions of all student repositories for a GitHub Classroom assignment, use `stoplight status`.\n\n```console\n$ stoplight status --org stoplight-demo --assignment-title assignment\nChecking Status  [####################################]  100%\n                         assignment                          \n┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━┓\n┃ Repo                       ┃ User            ┃ Permission ┃\n┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━┩\n│ assignment-Michionlion     │ Michionlion     │ write      │\n│ assignment-mariakimheinert │ mariakimheinert │ admin      │\n└────────────────────────────┴─────────────────┴────────────┘\n```\n\nNote that repositories whose names end with `starter` or `solution` or that are the assignment title are excluded.\n\nYou can also specify the organization and assignment title in your `.stoplightrc`.\n\n```toml\ntoken = "<TOKEN>"\norg = "stoplight-demo"\nassignment_title = "assignment"\n```\n\n```console\n$ stoplight status\nChecking Status  [####################################]  100%\n                         assignment                          \n┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━┓\n┃ Repo                       ┃ User            ┃ Permission ┃\n┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━┩\n│ assignment-Michionlion     │ Michionlion     │ write      │\n│ assignment-mariakimheinert │ mariakimheinert │ admin      │\n└────────────────────────────┴─────────────────┴────────────┘\n```\n\nOne way to use the `.stoplightrc` is to store it in a directory that you use to store starter and solution files for a GitHub Classroom assignment. Then, you can use `stoplight` from that directory to control the push access to that GitHub Classroom assignment. A `.stoplightrc` in the directory from which `stoplight` is executed will be given priority over a `.stoplightrc` in your home directory.\n\n#### `stoplight red`\n\nTo disable push access for all students to their GitHub Classroom assignment repositories, use `stoplight red`.\n\n```console\n$ stoplight red\nUpdating Permissions  [####################################]  100%\nChecking Status  [####################################]  100%\n                         assignment                          \n┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━┓\n┃ Repo                       ┃ User            ┃ Permission ┃\n┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━┩\n│ assignment-Michionlion     │ Michionlion     │ read       │\n│ assignment-mariakimheinert │ mariakimheinert │ admin      │\n└────────────────────────────┴─────────────────┴────────────┘\n```\n\nNotice that you cannot update the permissions of students who have admin access to their GitHub Classroom assignment repository. So, if you want to use `stoplight`, leave the following box unchecked when creating your GitHub Classroom assignment.\n\n![Setting](.github/admin-access.png)\n\n#### `stoplight green`\n\nTo enable push access for students to their GitHub Classroom assignment repositories, use `stoplight green [STUDENTS]...`.\n\n```console\n$ stoplight green Michionlion\nUpdating Permissions  [####################################]  100%\nChecking Status  [####################################]  100%\n                     assignment                      \n┏━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━┓\n┃ Repo                   ┃ User        ┃ Permission ┃\n┡━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━┩\n│ assignment-Michionlion │ Michionlion │ write      │\n└────────────────────────┴─────────────┴────────────┘\n```\n\nYou can also use the `--all` option to enable push access for all students.\n\n```console\n$ stoplight red\nUpdating Permissions  [####################################]  100%\nChecking Status  [####################################]  100%\n                         assignment                          \n┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━┓\n┃ Repo                       ┃ User            ┃ Permission ┃\n┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━┩\n│ assignment-Michionlion     │ Michionlion     │ read       │\n│ assignment-mariakimheinert │ mariakimheinert │ admin      │\n└────────────────────────────┴─────────────────┴────────────┘\n$ stoplight green --all\nUpdating Permissions  [####################################]  100%\nChecking Status  [####################################]  100%\n                         assignment                          \n┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━┓\n┃ Repo                       ┃ User            ┃ Permission ┃\n┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━┩\n│ assignment-Michionlion     │ Michionlion     │ write      │\n│ assignment-mariakimheinert │ mariakimheinert │ admin      │\n└────────────────────────────┴─────────────────┴────────────┘\n```\n\nFor additional information, use `stoplight --help`.\n',
    'author': 'Maria Kim Heinert',
    'author_email': 'yeeunmariakim@gmail.com',
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
