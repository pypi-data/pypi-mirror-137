# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_urlconfchecks', 'tests', 'tests.urls']

package_data = \
{'': ['*']}

extras_require = \
{':extra == "test" or extra == "dev"': ['django>=3.2.0'],
 'dev': ['tox>=3.20.1,<4.0.0',
         'virtualenv>=20.2.2,<21.0.0',
         'pip>=20.3.1,<21.0.0',
         'twine>=3.3.0,<4.0.0',
         'pre-commit>=2.12.0,<3.0.0',
         'toml>=0.10.2,<0.11.0',
         'bump2version>=1.0.1,<2.0.0'],
 'doc': ['mkdocs>=1.1.2,<2.0.0',
         'mkdocs-include-markdown-plugin>=3.2.3,<4.0.0',
         'mkdocs-material>=8.1.8,<9.0.0',
         'mkdocstrings>=0.17.0,<0.18.0',
         'mkdocs-autorefs>=0.2.1,<0.4.0'],
 'test': ['black>=21.5,<23.0',
          'isort>=5.8.0,<6.0.0',
          'flake8>=4.0.1,<5.0.0',
          'flake8-docstrings>=1.6.0,<2.0.0',
          'mypy>=0.931,<0.932',
          'pytest>=6.2.4,<7.0.0',
          'pytest-cov>=3.0.0,<4.0.0',
          'pyupgrade>=2.31.0,<3.0.0']}

setup_kwargs = {
    'name': 'django-urlconfchecks',
    'version': '0.3.0',
    'description': 'a python package for type checking the urls and associated views.',
    'long_description': "# django-UrlConfChecks\n\n[![pypi](https://img.shields.io/pypi/v/django-urlconfchecks.svg)](https://pypi.org/project/django-urlconfchecks/)\n[![python](https://img.shields.io/pypi/pyversions/django-urlconfchecks.svg)](https://pypi.org/project/django-urlconfchecks/)\n[![Build Status](https://github.com/AliSayyah/django-urlconfchecks/actions/workflows/dev.yml/badge.svg)](https://github.com/AliSayyah/django-urlconfchecks/actions/workflows/dev.yml)\n[![codecov](https://codecov.io/gh/AliSayyah/django-urlconfchecks/branch/main/graphs/badge.svg)](https://codecov.io/github/AliSayyah/django-urlconfchecks)\n[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/AliSayyah/django-urlconfchecks/main.svg)](https://results.pre-commit.ci/latest/github/AliSayyah/django-urlconfchecks/main)\n\na python package for type checking the urls and associated views\n\n* Documentation: <https://AliSayyah.github.io/django-urlconfchecks>\n* GitHub: <https://github.com/AliSayyah/django-urlconfchecks>\n* PyPI: <https://pypi.org/project/django-urlconfchecks/>\n* Free software: GPL3\n## Installation\n\n    pip install django-urlconfchecks\n\n## Usage\n\nAdd this to your settings.py imports:\n\n    import django_urlconfchecks\n## Features\n\nUsing this package, URL pattern types will automatically be matched with associated views, and in case of mismatch, an\nerror will be raised.\n\nExample:\n\n```python\n# urls.py\nfrom django.urls import path\n\nfrom . import views\n\nurlpatterns = [\n    path('articles/<str:year>/', views.year_archive),\n    path('articles/<int:year>/<int:month>/', views.month_archive),\n    path('articles/<int:year>/<int:month>/<slug:slug>/', views.article_detail),\n]\n```\n\n```python\n# views.py\n\ndef special_case(request):\n    pass\n\n\ndef year_archive(request, year: int):\n    pass\n\n\ndef month_archive(request, year: int, month: int):\n    pass\n\n\ndef article_detail(request, year: int, month: int, slug: str):\n    pass\n```\n\noutput will be:\n\n```\n(urlchecker.E002) For parameter `year`, annotated type int does not match expected `str` from urlconf\n```\n\n* TODO\n    - Fine-grained methods for silencing checks.\n    - Should only warn for each unhandled Converter once\n    - Regex patterns perhaps? (only RoutePattern supported at the moment)\n\n## Credits\n\n- [Luke Plant](https://github.com/spookylukey) for providing the idea and the initial code.\n- This package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and\n  the [waynerv/cookiecutter-pypackage](https://github.com/waynerv/cookiecutter-pypackage) project template.\n",
    'author': 'ali sayyah',
    'author_email': 'ali.sayyah2@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/AliSayyah/django-urlconfchecks',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.7.0,<4.0',
}


setup(**setup_kwargs)
