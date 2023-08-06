# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cognite',
 'cognite.utils',
 'cognite.utils.contextualization',
 'cognite.utils.infrastructure']

package_data = \
{'': ['*']}

install_requires = \
['cognite-sdk-experimental>=0.60.37,<0.61.0', 'cognite-sdk>=2.38.4,<3.0.0']

setup_kwargs = {
    'name': 'cognite-utils',
    'version': '0.1.0',
    'description': 'Python Utilities Extending the Use of Cognite Products',
    'long_description': 'Cognite Python Utilities\n========================\n[![Test and Build](https://github.com/cognitedata/cognite-python-utils/workflows/test_and_build/badge.svg)](https://github.com/cognitedata/cognite-python-utils/actions?query=workflow:test_and_build)\n[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-2.1-4baaaa.svg)](https://cognitedata.github.io/cognite-python-utils/development/covenant.html)\n[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\nThis is a package of utilities extending the use of Cognite products. Its aim is to assist\nCognite users with common/recurrent workflows and applications.\n\n## Directory Structure\n\n```\n├── cognite                         <- Source code\n│   └── utils\n│       ├── contextualization       <- Functionalities relating to contextualization\n│       ├── infrastructure          <- Functionalities relating to infrastructure\n│       ├── ...\n│       └── __init__.py\n```\n\n## Getting Started\n\nTo install this package, run:\n\n```bash\n$ pip install cognite-utils\n```\n\nOr, if using [poetry](https://python-poetry.org/docs/), run:\n\n```bash\n$ poetry add cognite-utils\n```\n\nThe following shows how you can load functionalities in the package:\n\n```python\n>>> from cognite.utils.contextualization import EntityMatchCategorizer\n>>> from cognite.utils.infrastructure import ProjectArchiver\n```\n\n## Documentation\n\n- [Cognite Python Utilities](https://cognitedata.github.io/cognite-python-utils/) (current project)\n- [Cognite Python SDK](https://cognite-docs.readthedocs-hosted.com/en/latest/)\n- [Cognite Python Experimental SDK](https://cognite-sdk-experimental.readthedocs-hosted.com/en/latest/)\n\nTo update project documentation, follow instructions [here](https://cognitedata.github.io/cognite-python-utils/development/basics.html#updating-project-documentation).\n\n## Contributing\n\nWant to contribute? Check out [Development](https://cognitedata.github.io/cognite-python-utils/development/index.html) page.\nAs an open source project, we abide by the [Contributor Covenant](https://cognitedata.github.io/cognite-python-utils/development/covenant.html).\n',
    'author': 'Sangyoon Park',
    'author_email': 'sangyoon.park@cognite.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://cognitedata.github.io/cognite-python-utils/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
