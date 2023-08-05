# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ipfabric', 'ipfabric.pathlookup', 'ipfabric.settings', 'ipfabric.tools']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.21.1,<0.22.0',
 'pydantic>=1.8.2,<2.0.0',
 'python-dateutil>=2.8.2,<3.0.0',
 'python-dotenv>=0.19.2,<0.20.0',
 'pytz>=2021.3,<2022.0']

setup_kwargs = {
    'name': 'ipfabric',
    'version': '0.7.0',
    'description': 'Python package for interacting with IP Fabric',
    'long_description': '# IPFabric\n\nIPFabric is a Python module for connecting to and communicating against an IP Fabric instance.\n\n## About\n\nFounded in 2015, [IP Fabric](https://ipfabric.io/) develops network infrastructure visibility and analytics solution to\nhelp enterprise network and security teams with network assurance and automation across multi-domain heterogeneous\nenvironments. From in-depth discovery, through graph visualization, to packet walks and complete network history, IP\nFabric enables to confidently replace manual tasks necessary to handle growing network complexity driven by relentless\ndigital transformation.\n\n## Installation\n\n```\npip install ipfabric\n```\n\n## Introduction\n\nPlease take a look at [API Programmability - Part 1: The Basics](https://ipfabric.io/blog/api-programmability-part-1/)\nfor instructions on creating an API token.\n\nMost of the methods and features can be located in [Examples](examples) to show how to use this package. \nAnother great introduction to this package can be found at [API Programmability - Part 2: Python](https://ipfabric.io/blog/api-programmability-python/)\n\n## Authentication\n### Basic\nPlease take a look at [basic.py](examples/basic.py) for basic authentication examples\n\n### Environment \nThe easiest way to use this package is with a `.env` file.  You can copy the sample and edit it with your environment variables. \n\n```commandline\ncp sample.env .env\n```\n\nThis contains the following variables which can also be set as environment variables instead of a .env file.\n```\nIPF_URL="https://demo3.ipfabric.io"\nIPF_TOKEN=TOKEN\nIPF_VERIFY=true\n```\n\n**`IPF_DEV` is an internal variable only, do not set to True.**\n\n## Development\n\nIPFabric uses poetry for the python packaging module. Install poetry globally:\n\n```\npip install poetry\n```\n\nTo install a virtual environment run the following command in the root of this directory.\n\n```\npoetry install\n```\n\nTo test and build:\n\n```\npoetry run pytest\npoetry build\n```\n\nGitHub Actions will publish and release. Make sure to tag your commits:\n\n* ci: Changes to our CI configuration files and scripts\n* docs: No changes just documentation\n* test: Added test cases\n* perf: A code change that improves performance\n* refactor: A code change that neither fixes a bug nor adds a feature\n* style: Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc)\n* fix: a commit of the type fix patches a bug in your codebase (this correlates with PATCH in Semantic Versioning). \n* feat: a commit of the type feat introduces a new feature to the codebase (this correlates with MINOR in Semantic Versioning). \n* BREAKING CHANGE: a commit that has a footer BREAKING CHANGE:, or appends a ! after the type/scope, introduces a breaking\nAPI change (correlating with MAJOR in Semantic Versioning). A BREAKING CHANGE can be part of commits of any type.\n',
    'author': 'Justin Jeffery',
    'author_email': 'justin.jeffery@ipfabric.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://ipfabric.io/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
