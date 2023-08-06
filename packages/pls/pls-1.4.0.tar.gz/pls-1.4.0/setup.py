# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pls', 'pls.data', 'pls.enums', 'pls.fs', 'pls.models']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0', 'rich>=11.1.0,<12.0.0']

entry_points = \
{'console_scripts': ['pls = pls.main:main']}

setup_kwargs = {
    'name': 'pls',
    'version': '1.4.0',
    'description': '`pls` is a better `ls` for developers.',
    'long_description': '<h1 align="center">\n  <img height="128px" src="https://raw.githubusercontent.com/dhruvkb/pls/main/readme_assets/pls.svg"/>\n</h1>\n\n<p align="center">\n  <a href="https://pypi.org/project/pls/">\n    <img src="https://img.shields.io/pypi/v/pls" alt="pls on PyPI"/>\n  </a>\n  <a href="https://www.python.org">\n    <img src="https://img.shields.io/pypi/pyversions/pls" alt="Python ^3.9"/>\n  </a>\n  <a href="https://github.com/dhruvkb/pls/blob/main/LICENSE">\n    <img src="https://img.shields.io/pypi/l/pls" alt="GPL-3.0-or-later"/>\n  </a>\n</p>\n\n<p align="center">\n  <img src="https://raw.githubusercontent.com/dhruvkb/pls/main/readme_assets/demo.png" alt="Demo of `pls`"/>\n</p>\n\n`pls` is a better `ls` for developers. The "p" stands for ("pro" as in "professional"/"programmer") or "prettier".\n\nIt works in a manner similar to `ls`, in  that it lists directories and files in a given directory, but it adds many more developer-friendly features.\n\nNote that `pls` is not a replacement for `ls`. `ls` is a tried, tested and trusted tool with lots of features. `pls`, on the other hand, is a simple tool for people who just want to see the contents of their directories.\n\n## Features\n\n`pls` provides many features over  `ls` command. `pls` can:\n\n- show Nerd Font icons or emoji next to files and directories making it easier to grep the output\n- colour output to further distinguish important files\n- use a more nuanced approach to hidden files than plainly hiding files with a leading dot `.`\n- groups directories and shows them all before files\n- ignores leading dots `.` and normalises case when sorting files\n- cascade specs by based on specificity levels\n- read `.pls.yml` files from the directory to augment its configuration\n\nThe icon, color and most behaviour in the application can be configured using plain-text YAML files for the pros who prefer to tweak their tools.\n\n## Upcoming features\n\nIn the future `pls` will be able to\n\n- generate visibility rules by parsing `.gitingore`\n- add MIME type as another method for matching files to specs\n- use complete path based matching for files\n- link files and hide derived files behind the main ones\n- support more columns like permissions, owner and size\n- support for tree-like output\n\nIf you want to help implement any of these features, feel free to submit a PR. `pls` is free and open-source software.\n',
    'author': 'Dhruv Bhanushali',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dhruvkb/pls',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
