# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['datetime_helpers']

package_data = \
{'': ['*']}

install_requires = \
['http-exceptions>=0.2.6,<0.3.0']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata<4.3']}

setup_kwargs = {
    'name': 'datetime-helpers',
    'version': '0.0.14',
    'description': 'Util for working with date and datetime objects',
    'long_description': "# Datetime Helpers\n\nA handy collection of datetime utils.\n\n[![Publish](https://github.com/DeveloperRSquared/datetime-helpers/actions/workflows/publish.yml/badge.svg)](https://github.com/DeveloperRSquared/datetime-helpers/actions/workflows/publish.yml)\n\n[![Python 3.7+](https://img.shields.io/badge/python-3.7+-brightgreen.svg)](#datetime-helpers)\n[![PyPI - License](https://img.shields.io/pypi/l/datetime-helpers.svg)](LICENSE)\n[![PyPI - Version](https://img.shields.io/pypi/v/datetime-helpers.svg)](https://pypi.org/project/datetime-helpers)\n\n[![CodeQL](https://github.com/DeveloperRSquared/datetime-helpers/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/DeveloperRSquared/datetime-helpers/actions/workflows/codeql-analysis.yml)\n[![codecov](https://codecov.io/gh/DeveloperRSquared/datetime-helpers/branch/main/graph/badge.svg?token=UI5ZDDDXXB)](https://codecov.io/gh/DeveloperRSquared/datetime-helpers)\n[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/DeveloperRSquared/datetime-helpers/main.svg)](https://results.pre-commit.ci/latest/github/DeveloperRSquared/datetime-helpers/main)\n\n[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)\n\n## Install\n\nInstall and update using [pip](https://pypi.org/project/datetime-helpers/).\n\n```sh\n$ pip install -U datetime-helpers\n```\n\n## What's available?\n\n```py\nimport datetime_helpers\n\n# Given a datetime:\n>>> dt = datetime.date(2017, 4, 17)\n\n# Check the day of week\n>>> datetime_helpers.get_day_of_week(dt=dt)\n'Monday'\n\n# Check if it is a weekend\n>>> datetime_helpers.is_weekend(dt=dt)\nFalse\n\n# Check if it is a weekday\n>>> datetime_helpers.is_weekday(dt=dt)\nTrue\n\n# Get the previous business day\n>>> datetime_helpers.get_previous_business_day(dt=dt)\ndatetime.date(2017, 4, 14)\n\n# Get the next business day\n>>> datetime_helpers.get_next_business_day(dt=dt)\ndatetime.date(2017, 4, 18)\n\n# Get the first business day of the month\n>>> datetime_helpers.get_first_business_day_of_month(dt=dt)\ndatetime.date(2017, 4, 3)\n\n# Get the nth business day of the month\n>>> n = 3  # e.g. third business day\n>>> datetime_helpers.get_nth_business_day_of_month(dt=dt, n=n)\ndatetime.date(2017, 4, 5)\n\n# Convert to a datetime string with custom format (defaults to JSON date format)\n>>> datetime_helpers.datetime_to_string(dt=dt)\n'2017-04-17T00:00:00.000000Z'\n\n# Convert to a date string with custom format (defaults to YYYY-MM-DD)\n>>> datetime_helpers.date_to_string(dt=dt)\n'2017-04-17'\n\n# Convert a string with custom format to datetime (defaults to JSON date format)\n>>> text = '2016-04-17T00:00:00.000000Z'\n>>> datetime_helpers.datetime_from_string(text=text)\ndatetime.datetime(2016, 4, 17, 0, 0)\n\n# Convert a string with custom format to datetime (defaults to JSON date format)\n>>> text = '2016-04-17T00:00:00.000000Z'\n>>> datetime_helpers.datetime_from_string(text=text)\ndatetime.datetime(2016, 4, 17, 0, 0)\n\n# Convert a windows filetime to datetime\n>>> windows_filetime = 116444736000000000\n>>> datetime_helpers.datetime_from_windows_filetime(windows_filetime=windows_filetime)\ndatetime.datetime(1970, 1, 1, 0, 0)\n\n# Convert to seconds\n>>> datetime_helpers.datetime_to_seconds(dt=dt)\n1492387200.0\n\n# Convert seconds to datetime\n>>> seconds = 1492387200\n>>> datetime_helpers.datetime_from_seconds(seconds=seconds)\ndatetime.datetime(2017, 4, 17, 0, 0)\n\n# Convert to millis\n>>> datetime_helpers.datetime_to_millis(dt=dt)\n1492387200000\n\n# Convert millis to datetime\n>>> millis = 1492387200000\n>>> datetime_helpers.datetime_from_millis(millis=millis)\ndatetime.datetime(2017, 4, 17, 0, 0)\n\n# Convert date to datetime\n>>> datetime_helpers.datetime_from_date(dt=dt)\ndatetime.datetime(2017, 4, 17, 0, 0)\n```\n\n## Contributing\n\nContributions are welcome via pull requests.\n\n### First time setup\n\n```sh\n$ git clone git@github.com:DeveloperRSquared/datetime-helpers.git\n$ cd datetime-helpers\n$ poetry install\n$ poetry shell\n```\n\nTools including black, mypy etc. will run automatically if you install [pre-commit](https://pre-commit.com) using the instructions below\n\n```sh\n$ pre-commit install\n$ pre-commit run --all-files\n```\n\n### Running tests\n\n```sh\n$ poetry run pytest\n```\n\n## Links\n\n- Source Code: <https://github.com/DeveloperRSquared/datetime-helpers/>\n- PyPI Releases: <https://pypi.org/project/datetime-helpers/>\n- Issue Tracker: <https://github.com/DeveloperRSquared/datetime-helpers/issues/>\n",
    'author': 'rikhilrai',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/DeveloperRSquared/datetime-helpers',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
