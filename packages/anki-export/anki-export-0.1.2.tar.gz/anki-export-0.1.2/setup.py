# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['anki_export']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'anki-export',
    'version': '0.1.2',
    'description': 'Export your Anki *.apkg to Python. Read Anki *.apkg in Python.',
    'long_description': "# anki-export\n\nExport your Anki \\*.apkg to Python. Read Anki \\*.apkg in Python.\n\n## Example\n\n```python\nfrom anki_export import ApkgReader\nimport pyexcel_xlsxwx\n\nwith ApkgReader('test.apkg') as apkg:\n    pyexcel_xlsxwx.save_data('test.xlsx', apkg.export(), config={'format': None})\n```\n\n## Installation\n\n```commandline\n$ pip install anki-export\n```\n\n## Why?\n\n- \\*.apkg is quite well structured, convincing me to use this format more.\n- Allow you to use \\*.apkg programmatically in Python.\n- Might be less buggy than https://github.com/patarapolw/AnkiTools\n\n## My other projects to create SRS flashcards outside Anki\n\n- [srs-sqlite](https://github.com/patarapolw/srs-sqlite) - A simple SRS app using Markdown/HandsOnTable/SQLite\n- [jupyter-flashcards](https://github.com/patarapolw/jupyter-flashcards) - Excel-powered. Editable in Excel. SRS-enabled.\n- [gflashcards](https://github.com/patarapolw/gflashcards) - A simple app to make formatted flashcards from Google Sheets. SRS-not-yet-enabled.\n- [HanziLevelUp](https://github.com/patarapolw/HanziLevelUp) - A Hanzi learning suite, with levels based on Hanzi Level Project, aka. another attempt to clone WaniKani.com for Chinese. SRS-enabled.\n",
    'author': 'patarapolw',
    'author_email': 'patarapolw@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
