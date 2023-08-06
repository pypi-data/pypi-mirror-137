# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mdc']

package_data = \
{'': ['*'], 'mdc': ['resources/*', 'templates/*']}

install_requires = \
['corgy[colors]>=4.4,<5.0']

extras_require = \
{':python_version < "3.9"': ['typing_extensions>=4.0,<5.0']}

entry_points = \
{'console_scripts': ['mathify = mdc:mathify', 'mdc = mdc.mdc:main']}

setup_kwargs = {
    'name': 'shinymdc',
    'version': '9.1.0',
    'description': 'Tool to compile markdown files to tex/pdf using pandoc, latexmk',
    'long_description': '# mdc\n\nMarkdown to tex/pdf compiler.\n',
    'author': 'Jayanth Koushik',
    'author_email': 'jnkoushik@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jayanthkoushik/mdc',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
