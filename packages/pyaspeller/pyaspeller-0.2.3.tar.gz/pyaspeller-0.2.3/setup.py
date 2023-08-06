# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pyaspeller']

package_data = \
{'': ['*']}

install_requires = \
['requests==2.27.1']

entry_points = \
{'console_scripts': ['pyaspeller = src.pyaspeller.__init__:main']}

setup_kwargs = {
    'name': 'pyaspeller',
    'version': '0.2.3',
    'description': 'Search tool typos in the text, files and websites.',
    'long_description': '# Python text speller\n\n[![CI](https://github.com/oriontvv/pyaspeller/workflows/Python%20package/badge.svg)](https://github.com/oriontvv/pyaspeller/actions)       [![Coverage Status](https://img.shields.io/coveralls/oriontvv/pyaspeller.svg)](https://coveralls.io/r/oriontvv/pyaspeller)         [![CodeQuality](https://codeclimate.com/github/oriontvv/pyaspeller/badges/gpa.svg)](https://codeclimate.com/github/oriontvv/pyaspeller)\n\n\n[![Pypi](http://img.shields.io/pypi/v/pyaspeller.svg?style=flat)](https://pypi.org/project/pyaspeller)     [![PyVersions](https://img.shields.io/pypi/pyversions/pyaspeller.svg)](https://img.shields.io/pypi/pyversions/pyaspeller.svg)\n\n\n[pyaspeller](https://github.com/oriontvv/pyaspeller) (Python Yandex Speller) is a cli tool and pure python library for searching typos in texts, files and websites.\n\nSpell checking uses [Yandex.Speller API](https://tech.yandex.ru/speller/doc/dg/concepts/About-docpage/). ([restrictions](<https://yandex.ru/legal/speller_api/>))\n\n\n## Features\n\n* Command line tool\n\nYou can correct your local files or web pages\n\n```bash \n$ pyaspeller ./doc\n$ pyaspeller https://team-tricky.github.io\n$ pyaspeller "в суббботу утромъ"\nв субботу утром\n```\n\n* Library \n\nUse speller for your code\n\n```python\n>>> from pyaspeller import YandexSpeller\n>>> speller = YandexSpeller()\n>>> fixed = speller.spelled(\'Triky Custle is a great puzzle game.\')\n>>> fixed\n\'Tricky Castle is a great puzzle game.\'\n```\n\nYou can use class `Word` for single word queries:\n\n```python\n>>> from pyaspeller import Word\n>>> check = Word(\'tesst\')\n>>> check.correct\nFalse\n>>> check.variants\n[u\'test\']\n>>> check.spellsafe\nu\'test\'\n```\n\n\n## Installation\n\nUse your favourite package manager:\n\n```bash\n$ python3 -m pip install pyaspeller\n```\n\nFor python2 you can use outdated version:\n\n```bash\n$ pip install pyaspeller==0.1.0\n```\n\nAlso there are available [rust](https://github.com/oriontvv/ryaspeller/) and [javascript](https://github.com/hcodes/yaspeller) versions of this speller.\n',
    'author': 'Vassiliy Taranov',
    'author_email': 'taranov.vv@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/oriontvv/pyaspeller',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
