# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['aws_lambda_requests_wrapper']

package_data = \
{'': ['*']}

install_requires = \
['case-insensitive-dictionary>=0.1.1,<0.2.0',
 'datetime-helpers>=0.0.14,<0.0.15',
 'pydantic>=1.9.0,<2.0.0']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata<4.3']}

setup_kwargs = {
    'name': 'aws-lambda-requests-wrapper',
    'version': '0.2.3',
    'description': 'Request/Response wrapper for AWS Lambda with API Gateway',
    'long_description': '# AWS Lambda Requests Wrapper\n\nRequest/Response wrapper for AWS Lambda with API Gateway.\n\n[![Publish](https://github.com/DeveloperRSquared/aws-lambda-requests-wrapper/actions/workflows/publish.yml/badge.svg)](https://github.com/DeveloperRSquared/aws-lambda-requests-wrapper/actions/workflows/publish.yml)\n\n[![Python 3.7+](https://img.shields.io/badge/python-3.7+-brightgreen.svg)](#aws-lambda-requests-wrapper)\n[![PyPI - License](https://img.shields.io/pypi/l/aws-lambda-requests-wrapper.svg)](LICENSE)\n[![PyPI - Version](https://img.shields.io/pypi/v/aws-lambda-requests-wrapper.svg)](https://pypi.org/project/aws-lambda-requests-wrapper)\n\n[![codecov](https://codecov.io/gh/DeveloperRSquared/aws-lambda-requests-wrapper/branch/main/graph/badge.svg?token=UI5ZDDDXXB)](https://codecov.io/gh/DeveloperRSquared/aws-lambda-requests-wrapper)\n[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/DeveloperRSquared/aws-lambda-requests-wrapper/main.svg)](https://results.pre-commit.ci/latest/github/DeveloperRSquared/aws-lambda-requests-wrapper/main)\n[![CodeQL](https://github.com/DeveloperRSquared/aws-lambda-requests-wrapper/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/DeveloperRSquared/aws-lambda-requests-wrapper/actions/workflows/codeql-analysis.yml)\n\n[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)\n\n## Install\n\nInstall and update using [pip](https://pypi.org/project/aws-lambda-requests-wrapper/).\n\n```sh\n$ pip install -U aws-lambda-requests-wrapper\n```\n\n## Example\n\nConverts the lambda_handler syntax:\n\n```py\nimport json\n\ndef lambda_handler(event, context):\n    ...\n    response = {"key": "value"}\n    return {\n        "statusCode": 200,\n        "headers": {\n            "Content-Type": "application/json"\n        },\n        "body": json.dumps(response)\n    }\n```\n\ninto this:\n\n```py\nimport json\n\nfrom aws_lambda_requests_wrapper.lambda_handler import lambda_request_wrapper\nfrom aws_lambda_requests_wrapper.models import Request\nfrom aws_lambda_requests_wrapper.models import Response\n\n@lambda_request_wrapper()\ndef lambda_handler(request: Request) -> Response:\n    ...\n    response = {"key": "value"}\n    return Response(body=json.dumps(response))\n```\n\nor return a Pydantic model directly:\n\n```py\nfrom pydantic import BaseModel\n\nfrom aws_lambda_requests_wrapper.lambda_handler import lambda_request_wrapper\nfrom aws_lambda_requests_wrapper.models import Request\n\nclass Model(BaseModel):\n    model_id: int\n\n@lambda_request_wrapper()\ndef get_pydantic_model(request: Request) -> Model:\n    return Model(model_id=1)\n```\n\n## Contributing\n\nContributions are welcome via pull requests.\n\n### First time setup\n\n```sh\n$ git clone git@github.com:DeveloperRSquared/aws-lambda-requests-wrapper.git\n$ cd aws-lambda-requests-wrapper\n$ poetry install\n$ source .venv/bin/activate\n```\n\nTools including black, mypy etc. will run automatically if you install [pre-commit](https://pre-commit.com) using the instructions below\n\n```sh\n$ pre-commit install\n$ pre-commit run --all-files\n```\n\n### Running tests\n\n```sh\n$ poetry run pytest\n```\n\n## Links\n\n- Source Code: <https://github.com/DeveloperRSquared/aws-lambda-requests-wrapper/>\n- PyPI Releases: <https://pypi.org/project/aws-lambda-requests-wrapper/>\n- Issue Tracker: <https://github.com/DeveloperRSquared/aws-lambda-requests-wrapper/issues/>\n',
    'author': 'rikhilrai',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/DeveloperRSquared/aws-lambda-requests-wrapper',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
