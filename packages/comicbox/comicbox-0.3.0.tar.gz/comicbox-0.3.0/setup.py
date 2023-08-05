# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['comicbox', 'comicbox.metadata', 'tests']

package_data = \
{'': ['*'], 'tests': ['test_files/*', 'test_files/Captain Science 001/*']}

install_requires = \
['parse>=1.15,<2.0',
 'pycountry>=22.1.3,<23.0.0',
 'rarfile>=4.0,<5.0',
 'simplejson>=3.17,<4.0']

entry_points = \
{'console_scripts': ['comicbox = comicbox.cli:main']}

setup_kwargs = {
    'name': 'comicbox',
    'version': '0.3.0',
    'description': 'An API for reading comic archives',
    'long_description': '# Comicbox\n\nComicbox is a comic book archive metadata reader and writer. It reads CBR and CBZ archives and writes CBZ archives. It reads and writes the [ComicRack comicinfo.xml format](https://wiki.mobileread.com/wiki/ComicRack#Metadata), the [ComicBookInfo format](https://code.google.com/archive/p/comicbookinfo/) and [CoMet format](https://github.com/wdhongtw/comet-utils).\n\n## ⌨️ <a href="usage">Usage</a>\n\n### API\n\nComicbox\'s primary purpose is as a library for other programs with [comicbox.comic_archive](https://github.com/ajslater/comicbox/blob/master/comicbox/comic_archive.py) as the primary interface.\n\n### Console\n\n```sh\ncomicbox -h\n```\n\nto use the CLI.\n\n## 🛠 <a href="development">Development</a>\n\nrun\n\n```sh\n./setup.sh\n```\n\nto get started.\n\nTo run the code you\'ve checked out\n\n```sh\n./run.sh -h\n```\n\nwill run the comicbox cli.\n\nI\'ll only merge branches to develop that pass\n\n```sh\n./lint.sh\n./test.sh\n./build.sh\n```\n\nAnd I might require tests for significant new code.\n\nYou may automatically fix most simple linting errors with\n\n```sh\n./fix-linting.sh\n```\n\n## 🤔 <a href="motivation">Motivation</a>\n\nI didn\'t like Comictagger\'s API, so I built this for myself as an educational exercise and to use as a library for [Codex comic reader](https://github.com/ajslater/codex/).\n\n## 👍🏻 <a href="alternative">Alternatives</a>\n\n[Comictagger](https://github.com/comictagger/comictagger) is a better alternative for most purposes at this time. It does everything Comicbox does but also automatically tags comics with the ComicVine API and has a pretty nice desktop UI.\n',
    'author': 'AJ Slater',
    'author_email': 'aj@slater.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ajslater/comicbox',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
