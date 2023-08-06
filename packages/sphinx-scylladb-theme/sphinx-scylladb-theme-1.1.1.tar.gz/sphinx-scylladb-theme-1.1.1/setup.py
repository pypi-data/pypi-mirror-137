# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sphinx_scylladb_theme',
 'sphinx_scylladb_theme.extensions',
 'sphinx_scylladb_theme.lexers']

package_data = \
{'': ['*'],
 'sphinx_scylladb_theme': ['static/css/*',
                           'static/img/*',
                           'static/img/icons/*',
                           'static/img/mascots/*',
                           'static/js/*']}

install_requires = \
['Sphinx>=4.3.2,<5.0.0',
 'beautifulsoup4>=4.10.0,<5.0.0',
 'pyyaml>=6.0,<7.0',
 'sphinx-collapse>=0.1.1,<0.2.0',
 'sphinx-copybutton>=0.4.0,<0.5.0',
 'sphinx-notfound-page>=0.8,<0.9',
 'sphinx-tabs>=3.2.0,<4.0.0']

setup_kwargs = {
    'name': 'sphinx-scylladb-theme',
    'version': '1.1.1',
    'description': 'A Sphinx Theme for ScyllaDB documentation projects',
    'long_description': '===================\nScylla Sphinx Theme\n===================\n\nSphinx theme for Scylla documentation projects.\n\n`Read More: <https://github.com/scylladb/sphinx-scylladb-theme>`_\n',
    'author': 'David García',
    'author_email': 'hi@davidgarcia.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
