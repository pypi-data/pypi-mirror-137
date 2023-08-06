# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fastapi_restful']

package_data = \
{'': ['*']}

install_requires = \
['fastapi>=0,<1', 'psutil>=5,<6', 'pydantic>=1,<2']

extras_require = \
{':python_full_version >= "3.6.2" and python_full_version < "3.7.0"': ['dataclasses>=0.8,<0.9'],
 'all': ['sqlalchemy>=1,<2'],
 'session': ['sqlalchemy>=1,<2']}

setup_kwargs = {
    'name': 'fastapi-restful',
    'version': '0.4.2',
    'description': 'Quicker FastApi developing tools',
    'long_description': '<p align="center">\n    <em>Quicker FastApi developing tools</em>\n</p>\n<p align="center">\n<a href="https://github.com/yuval9313/fastapi-restful" target="_blank">\n\t<img src="https://img.shields.io/github/last-commit/yuval9313/fastapi-restful.svg">\n\t<img src="https://github.com/yuval9313/FastApi-RESTful/workflows/build/badge.svg" alt="Build CI">\n</a>\n<a href="https://fastapi-restful.netlify.app">\n    <img src="https://api.netlify.com/api/v1/badges/294b88e1-4b81-49c0-8525-9c4a2cb782e0/deploy-status" alt="Netlify status">\n</a>\n<br />\n<a href="https://pypi.org/project/FastApi-RESTful" target="_blank">\n    <img src="https://badge.fury.io/py/fastapi-restful.svg" alt="Package version">\n</a>\n<a href="https://github.com/yuval9313/fastapi-restful" target="_blank">\n    <img src="https://img.shields.io/pypi/pyversions/FastApi-RESTful.svg" alt="Python versions">\n    <img src="https://img.shields.io/github/license/yuval9313/fastapi-utils.svg" alt="License">\n</a>\n</p>\n\n---\n\n**Documentation**: <a href="https://fastapi-restful.netlify.app" target="_blank">https://fastapi-restful.netlify.app</a>\n\n**Source Code**: <a href="https://github.com/yuval9313/fastapi-restful" target="_blank">https://github.com/yuval9313/fastapi-restful</a>\n\nBase on: <a href="https://github.com/dmontagu/fastapi-utils" target="_blank">https://github.com/dmontagu/fastapi-utils</a>\n\n---\n\n<a href="https://fastapi.tiangolo.com">FastAPI</a> is a modern, fast web framework for building APIs with Python 3.6+.\n\nBut if you\'re here, you probably already knew that!\n\n---\n\n## Features\n\nThis package includes a number of utilities to help reduce boilerplate and reuse common functionality across projects:\n\n* **Resource Class**: Create CRUD with ease the OOP way with `Resource` base class that lets you implement methods quick.\n* **Class Based Views**: Stop repeating the same dependencies over and over in the signature of related endpoints.\n* **Response-Model Inferring Router**: Let FastAPI infer the `response_model` to use based on your return type annotation. \n* **Repeated Tasks**: Easily trigger periodic tasks on server startup\n* **Timing Middleware**: Log basic timing information for every request\n* **OpenAPI Spec Simplification**: Simplify your OpenAPI Operation IDs for cleaner output from OpenAPI Generator\n* **SQLAlchemy Sessions**: The `FastAPISessionMaker` class provides an easily-customized SQLAlchemy Session dependency\n\n---\n\nIt also adds a variety of more basic utilities that are useful across a wide variety of projects:\n\n* **APIModel**: A reusable `pydantic.BaseModel`-derived base class with useful defaults\n* **APISettings**: A subclass of `pydantic.BaseSettings` that makes it easy to configure FastAPI through environment variables \n* **String-Valued Enums**: The `StrEnum` and `CamelStrEnum` classes make string-valued enums easier to maintain\n* **CamelCase Conversions**: Convenience functions for converting strings from `snake_case` to `camelCase` or `PascalCase` and back\n* **GUID Type**: The provided GUID type makes it easy to use UUIDs as the primary keys for your database tables\n\nSee the [docs](https://fastapi-restful.netlify.app/) for more details and examples. \n\n## Requirements\n\nThis package is intended for use with any recent version of FastAPI (depending on `pydantic>=1.0`), and Python 3.6+.\n\n## Installation\n\n```bash\npip install fastapi-restful  # For basic slim package :)\n\npip install fastapi-restful[session]  # To add sqlalchemy session maker\n\npip install fastapi-restful[all]  # For all the packages\n```\n\n## License\n\nThis project is licensed under the terms of the MIT license.\n',
    'author': 'Yuval Levi',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://fastapi-restful.netlify.app',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
