# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wordlerer']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.9.0,<2.0.0', 'selenium>=4.1.0,<5.0.0']

setup_kwargs = {
    'name': 'wordlerer',
    'version': '0.1.0',
    'description': 'Wordlerer can automatically solve wordle puzzle in the browser.',
    'long_description': '# Wordlerer\n\nWordlerer can automatically solve wordle puzzle in the browser.\n\n## Installation\n\n```shell\npip install wordlerer\n```\n\n## Usage\n\n```python\nfrom wordlerer import BrowserApp\n\nBrowserApp().run()\n```\n',
    'author': 'Tibor Mikita',
    'author_email': 'tibor@mikita.eu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/hoou/wordlerer',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
