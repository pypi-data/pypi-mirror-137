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
    'version': '1.6.0',
    'description': '`pls` is a better `ls` for developers.',
    'long_description': '<h1 align="center">\n  <img height="128px" src="https://raw.githubusercontent.com/dhruvkb/pls/main/readme_assets/pls.svg"/>\n</h1>\n\n<p align="center">\n  <a href="https://pypi.org/project/pls/">\n    <img src="https://img.shields.io/pypi/v/pls" alt="pls on PyPI"/>\n  </a>\n  <a href="https://www.python.org">\n    <img src="https://img.shields.io/pypi/pyversions/pls" alt="Python versions"/>\n  </a>\n  <a href="https://github.com/dhruvkb/pls/blob/main/LICENSE">\n    <img src="https://img.shields.io/pypi/l/pls" alt="GPL-3.0-or-later"/>\n  </a>\n</p>\n\n<p align="center">\n  <img src="https://raw.githubusercontent.com/dhruvkb/pls/main/readme_assets/demo.png" alt="Demo of `pls`"/>\n</p>\n\n`pls` is a better `ls` for developers. The "p" stands for ("pro" as in "professional"/"programmer") or "prettier".\n\nIt works in a manner similar to `ls`, in  that it lists directories and files in a given directory, but it adds many more developer-friendly features.\n\nNote that `pls` is not a replacement for `ls`. `ls` is a tried, tested and trusted tool with lots of features. `pls`, on the other hand, is a simple tool for people who just want to see the contents of their directories.\n\n## Features\n\n`pls` provides many features over  `ls` command. `pls` can:\n\n- show Nerd Font icons or emoji next to files and directories making it easier to grep the output\n- colour output to further distinguish important files\n- use a more nuanced approach to hidden files than plainly hiding files with a leading dot `.`\n- groups directories and shows them all before files\n- ignores leading dots `.` and normalises case when sorting files\n- cascade specs by based on specificity levels\n- read `.pls.yml` files from the directory to augment its configuration\n- show more details like permissions, owner and size in columns\n\nThe icon, color and most behaviour in the application can be configured using plain-text YAML files for the pros who prefer to tweak their tools.\n\n## Upcoming features\n\nIn the future `pls` will be able to\n\n- generate visibility rules by parsing `.gitingore`\n- add MIME type as another method for matching files to specs\n- use complete path based matching for files\n- link files and hide derived files behind the main ones\n- support for tree-like output\n\nIf you want to help implement any of these features, feel free to submit a PR. `pls` is free and open-source software.\n\n## Installation\n\nTo get the best of `pls`, [install a Nerd Font](https://github.com/ryanoasis/nerd-fonts/blob/master/readme.md#font-installation) on your computer. [Nerd Fonts](https://www.nerdfonts.com) come patched with many icons from different popular icon sets. If you\'re a "pro" (the target audience for `pls`) these fonts are basically a must.\n\n`pls` is a pure-Python codebase and is deployed to PyPI. So installing it on any system with a supported Python version is quite straightforward.\n\n```shell\n$ python3 -m pip install --user pls\n```\n\nThere are no native packages _yet_.\n\n## Usage\n\n`pls` has a very simple API with easy to memorise flags. There are no mandatory arguments. Just run `pls` anywhere on your disk.\n\n```shell\n$ pls\n```\n\nThere are a few optional arguments and flags you can use to tweak the behaviour. You can see the complete list of arguments and their description by passing the `--help` or `-h` flags.\n\n```shell\n$ pls --help\n```\n\n### Directory\n\nThe only positional argument is a directory. Pass this to see the contents of a different folder rather than the current working directory.\n\n```shell\n$ pls path/to/somewhere/else\n```\n\n### Icons\n\n`pls` supports many icons for popular languages out of the box and will show icons by default. If you don\'t have a Nerd Font (why?), you can switch to emoji icons using `--icons emoji` or `-iemoji`. Be warned they are quite bad. If you are a sad person, you turn icons off using `--icon none` or `-inone`.\n\n**Note:** The built-in icon configuration is intentionally lean. The whole idea is for `pls` to be [customisable by you](pls/data/README.md).\n\n### Filtering\n\nYou can choose to hide files or folders from the output using `--no-files` and `--no-dirs` respectively. Passing both will lead to a blank output.\n\n### Sorting\n\nBy default `pls` will place all directories first, followed by files with both sorted alphabetically from A to Z. You can prevent folders from being first by passing the `--no-dirs-first` flag. You can change the sort to go from Z to A using `--sort desc` or `-sdesc`. Leading dots are ignored during sorting.\n\n### Alignment\n\nA lot of code related files start with a leading dot `.` for no valid reason. `pls` by default\n\n- lists those files\n- moves their name left by one character to line up the actual alphabets\n- dims their leading dot\n\nIf you don\'t like this, you can set `--no-align` to turn off all this behaviour in one swoop.\n\n### Details\n\nWhen you need more infomation about your files, pass the `--details` flag. This expands the list into a table, with\n\n- permissions\n- owner name\n- size\n\nadded to the output. The permissions are presented as `rwx` triplets. The size is presented in binary compound-units (the ones with the "i" like "*iB"). You can switch to decimal units by passing `--units decimal` or `-udecimal`. This flag has no effect unless the `--detail` flag is passed too.\n',
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
