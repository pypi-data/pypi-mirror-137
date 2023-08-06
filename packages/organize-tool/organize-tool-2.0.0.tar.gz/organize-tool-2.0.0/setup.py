# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['organize', 'organize.actions', 'organize.filters']

package_data = \
{'': ['*']}

install_requires = \
['ExifRead>=2.3.2,<3.0.0',
 'Jinja2>=3.0.3,<4.0.0',
 'PyYAML>=5.4.1,<6.0.0',
 'Send2Trash>=1.8.0,<2.0.0',
 'click>=8.0.3,<9.0.0',
 'fs>=2.4.14,<3.0.0',
 'rich>=11.0.0,<12.0.0',
 'schema>=0.7.5,<0.8.0',
 'simplematch>=1.3,<2.0']

extras_require = \
{':sys_platform == "darwin"': ['macos-tags>=1.5.1,<2.0.0'],
 'docs': ['mkdocs>=1.2.3,<2.0.0',
          'mkdocstrings>=0.17.0,<0.18.0',
          'mkdocs-include-markdown-plugin>=3.2.3,<4.0.0',
          'mkdocs-autorefs>=0.3.1,<0.4.0'],
 'textract': ['textract>=1.6.4,<2.0.0']}

entry_points = \
{'console_scripts': ['organize = organize.cli:cli']}

setup_kwargs = {
    'name': 'organize-tool',
    'version': '2.0.0',
    'description': 'The file management automation tool',
    'long_description': '<p align="center">\n  <img width="623" height="168" src="https://github.com/tfeldmann/organize/raw/gh-pages/img/organize.svg?sanitize=true" alt="organize logo">\n</p>\n\n<div align="center">\n\n<a href="https://github.com/tfeldmann/organize/actions/workflows/tests.yml">\n  <img src="https://github.com/tfeldmann/organize/actions/workflows/tests.yml/badge.svg" title="tests">\n</a>\n<a href="https://organize.readthedocs.io/en/latest/?badge=latest">\n  <img src="https://readthedocs.org/projects/organize/badge/?version=latest" title="Documentation Status">\n</a>\n<a href="https://github.com/tfeldmann/organize/blob/main/LICENSE.txt">\n  <img src="https://img.shields.io/badge/license-MIT-blue.svg" title="License">\n</a>\n<a href="https://pypi.org/project/organize-tool/">\n  <img src="https://img.shields.io/pypi/v/organize-tool" title="PyPI Version">\n</a>\n\n</div>\n\n---\n\n<p align="center"> <b>organize</b> - The file management automation tool\n<br>\n<a href="https://organize.readthedocs.io/" target="_blank">Full documentation at Read the docs</a>\n</p>\n\n## **organize v2 is released!**\n\nThis is a huge update with lots of improvements.\nPlease backup all your important stuff before running and use the simulate option!\n\n- [See the changelog](https://organize.readthedocs.io/en/v2/changelog/) for all the new\n  features!\n- [Migration guide](docs/updating-from-v1.md) from organize v1\n\n## About\n\nYour desktop is a mess? You cannot find anything in your downloads and\ndocuments? Sorting and renaming all these files by hand is too tedious?\nTime to automate it once and benefit from it forever.\n\n**organize** is a command line, open-source alternative to apps like Hazel (macOS)\nor File Juggler (Windows).\n\n## Features\n\nSome highlights include:\n\n- Safe moving, renaming, copying of files and folders with conflict resolution options\n- Fast duplicate file detection\n- Exif tags extraction\n- Categorization via text extracted from PDF, DOCX and many more\n- Supports remote file locations like FTP, WebDAV, S3 Buckets, SSH and many more\n- Powerful template engine\n- Inline python and shell commands as filters and actions for maximum flexibility\n- Everything can be simulated before touching your files.\n\n## Getting started\n\n### Installation\n\nPython 3.6+ is needed. Install it via your package manager or from [python.org](https://python.org).\n\nInstallation is done via pip. Note that the package name is `organize-tool`:\n\n```bash\npip3 install -U organize-tool\n```\n\nIf you want the text extraction capabilities, install with `textract` like this:\n\n```bash\npip3 install -U "organize-tool[textract]"\n```\n\nThis command can also be used to update to the newest version. Now you can run `organize --help` to check if the installation was successful.\n\n### Create your first rule\n\nIn your shell, run `organize edit` to edit the configuration:\n\n```yaml\nrules:\n  - name: "Find PDFs"\n    locations:\n      - ~/Downloads\n    subfolders: true\n    filters:\n      - extension: pdf\n    actions:\n      - echo: "Found PDF!"\n```\n\n> If you have problems editing the configuration you can run `organize reveal` to reveal the configuration folder in your file manager. You can then edit the `config.yaml` in your favourite editor.\n\nsave your config file and run:\n\n```sh\norganize run\n```\n\nYou will see a list of all `.pdf` files you have in your downloads folder (+ subfolders).\nFor now we only show the text `Found PDF!` for each file, but this will change soon...\n(If it shows `Nothing to do` you simply don\'t have any pdfs in your downloads folder).\n\nRun `organize edit` again and add a `move`-action to your rule:\n\n```yml\nactions:\n  - echo: "Found PDF!"\n  - move: ~/Documents/PDFs/\n```\n\nNow run `organize sim` to see what would happen without touching your files.\n\nYou will see that your pdf-files would be moved over to your `Documents/PDFs` folder.\n\nCongratulations, you just automated your first task. You can now run `organize run`\nwhenever you like and all your pdfs are a bit more organized. It\'s that easy.\n\n> There is so much more. You want to rename / copy files, run custom shell- or python scripts, match names with regular expressions or use placeholder variables? organize has you covered. Have a look at the advanced usage example below!\n\n## Example rules\n\nHere are some examples of simple organization and cleanup rules. Modify to your needs!\n\nMove all invoices, orders or purchase documents into your documents folder:\n\n```yaml\nrules:\n  - name: "Sort my invoices and receipts"\n    locations: ~/Downloads\n    subfolders: true\n    filters:\n      - extension: pdf\n      - name:\n          contains:\n            - Invoice\n            - Order\n            - Purchase\n          case_sensitive: false\n    actions:\n      - move: ~/Documents/Shopping/\n```\n\nRecursively delete all empty directories:\n\n```yaml\nrules:\n  - name: "Recursively delete all empty directories"\n    locations:\n      - path: ~/Downloads\n    subfolders: true\n    filters:\n      - empty\n    actions:\n      - delete\n```\n\n<!--<details markdown="1">\n  <summary markdown="1">Advanced example</summary>\n\nThis example shows some advanced features like placeholder variables, pluggable\nactions, limited recursion through subfolders and filesystems (FTP and ZIP):\n\nThis rule:\n\n- Searches recursively in your documents folder (three levels deep) and on a FTP server\n- for files with **pdf** or **docx** extension\n- that have a created timestamp\n- Asks for user confirmation for each file\n- Moves them according to their extensions and **created** timestamps:\n- `script.docx` will be moved to `~/Documents/DOCX/2018-01/script.docx`\n- `demo.pdf` will be moved to `~/Documents/PDF/2016-12/demo.pdf`\n- If this new is already taken, a counter is appended to the filename ("rename_new")\n- Creates a zip backup file on your desktop containing all files.\n\n```yaml\nrules:\n  - name: "Download, cleanup and backup"\n    locations:\n      - path: ~/Documents\n        max_depth: 3\n      - path: ftps://demo:demo@demo.wftpserver.com\n    filters:\n      - extension:\n          - pdf\n          - docx\n      - created\n    actions:\n      - confirm:\n          msg: "Really continue?"\n          default: true\n      - move:\n          dest: "~/Documents/{extension.upper()}/{created.strftime(\'%Y-%m\')}/"\n          on_conflict: rename_new\n      - copy: "zip:///Users/thomas/Desktop/backup.zip"\n```\n\n</details>-->\n\nYou\'ll find many more examples in the <a href="https://tfeldmann.github.io/organize" target="_blank">full documentation</a>.\n\n## Command line interface\n\n```sh\nUsage: organize [OPTIONS] COMMAND [ARGS]...\n\n  organize\n\n  The file management automation tool.\n\nOptions:\n  --version   Show the version and exit.\n  -h, --help  Show this message and exit.\n\nCommands:\n  run     Organizes your files according to your rules.\n  sim     Simulates a run (does not touch your files).\n  edit    Edit the rules.\n  check   Checks whether a given config file is valid.\n  reveal  Reveals the default config file.\n  schema  Prints the json schema for config files.\n  docs    Opens the documentation.\n```\n',
    'author': 'Thomas Feldmann',
    'author_email': 'mail@tfeldmann.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tfeldmann/organize',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
