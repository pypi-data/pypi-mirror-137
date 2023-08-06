# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fbv']

package_data = \
{'': ['*']}

install_requires = \
['django>2.2.0']

extras_require = \
{'docs': ['Sphinx>=4.3.2,<5.0.0',
          'linkify-it-py>=1.0.3,<2.0.0',
          'myst-parser>=0.16.1,<0.17.0',
          'furo>=2021.11.23,<2022.0.0',
          'sphinx-copybutton>=0.4.0,<0.5.0',
          'toml']}

setup_kwargs = {
    'name': 'django-fbv',
    'version': '0.4.0',
    'description': 'Utilities to make function-based views cleaner, more efficient, and better tasting. ',
    'long_description': '<p align="center">\n  <a href="https://django-fbv.readthedocs.io"><h1 align="center">django-fbv</h1></a>\n</p>\n<p align="center">Utilities to make Django function-based views cleaner, more efficient, and better tasting. 💥</p>\n\n![PyPI](https://img.shields.io/pypi/v/django-fbv?color=blue&style=flat-square)\n![PyPI - Downloads](https://img.shields.io/pypi/dm/django-fbv?color=blue&style=flat-square)\n![GitHub Sponsors](https://img.shields.io/github/sponsors/adamghill?color=blue&style=flat-square)\n\n📖 Complete documentation: https://django-fbv.readthedocs.io\n\n📦 Package located at https://pypi.org/project/django-fbv/\n\n## Features\n\n### decorators\n\n- [`fbv.decorators.render_html`](https://django-fbv.readthedocs.io/en/latest/decorators/#render-html): decorator to specify the template that a view function response should use when rendering\n- [`fbv.decorators.render_view`](https://django-fbv.readthedocs.io/en/latest/decorators/#render-view): decorator to specify the template and content type that a view function response should use when rendering\n- [`fbv.decorators.render_json`](https://django-fbv.readthedocs.io/en/latest/decorators/#render-json): decorator to automatically render dictionaries, Django Models, or Django QuerySets as a JSON response\n\n### views\n\n- [`fbv.views.html_view`](https://django-fbv.readthedocs.io/en/latest/views/#html-view): directly render a template from `urls.py`\n- [`fbv.views.favicon_file`](https://django-fbv.readthedocs.io/en/latest/views/#favicon-file): serve an image file as the favicon.ico\n- [`fbv.views.favicon_emoji`](https://django-fbv.readthedocs.io/en/latest/views/#favicon-emoji): serve an emoji as the favicon.ico\n\n### middleware\n\n- [`fbv.middleware.RequestMethodMiddleware`](https://django-fbv.readthedocs.io/en/latest/middleware/): adds a boolean property to the `request` for the current request\'s HTTP method\n\nRead all of the documentation at https://django-fbv.readthedocs.io/.\n',
    'author': 'adamghill',
    'author_email': 'adam@adamghill.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/adamghill/django-fbv/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
