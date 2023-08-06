<h1 align="center">
  <img height="128px" src="https://raw.githubusercontent.com/dhruvkb/pls/main/readme_assets/pls.svg"/>
</h1>

<p align="center">
  <a href="https://pypi.org/project/pls/">
    <img src="https://img.shields.io/pypi/v/pls" alt="pls on PyPI"/>
  </a>
  <a href="https://www.python.org">
    <img src="https://img.shields.io/pypi/pyversions/pls" alt="Python versions"/>
  </a>
  <a href="https://github.com/dhruvkb/pls/blob/main/LICENSE">
    <img src="https://img.shields.io/pypi/l/pls" alt="GPL-3.0-or-later"/>
  </a>
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/dhruvkb/pls/main/readme_assets/demo.png" alt="Demo of `pls`"/>
</p>

`pls` is a better `ls` for developers. The "p" stands for ("pro" as in "professional"/"programmer") or "prettier".

It works in a manner similar to `ls`, in  that it lists directories and files in a given directory, but it adds many more developer-friendly features.

Note that `pls` is not a replacement for `ls`. `ls` is a tried, tested and trusted tool with lots of features. `pls`, on the other hand, is a simple tool for people who just want to see the contents of their directories.

## Features

`pls` provides many features over  `ls` command. `pls` can:

- show Nerd Font icons or emoji next to files and directories making it easier to grep the output
- colour output to further distinguish important files
- use a more nuanced approach to hidden files than plainly hiding files with a leading dot `.`
- groups directories and shows them all before files
- ignores leading dots `.` and normalises case when sorting files
- cascade specs by based on specificity levels
- read `.pls.yml` files from the directory to augment its configuration
- show more details like permissions, owner and size in columns

The icon, color and most behaviour in the application can be configured using plain-text YAML files for the pros who prefer to tweak their tools.

## Upcoming features

In the future `pls` will be able to

- generate visibility rules by parsing `.gitingore`
- add MIME type as another method for matching files to specs
- use complete path based matching for files
- link files and hide derived files behind the main ones
- support for tree-like output

If you want to help implement any of these features, feel free to submit a PR. `pls` is free and open-source software.

## Installation

To get the best of `pls`, [install a Nerd Font](https://github.com/ryanoasis/nerd-fonts/blob/master/readme.md#font-installation) on your computer. [Nerd Fonts](https://www.nerdfonts.com) come patched with many icons from different popular icon sets. If you're a "pro" (the target audience for `pls`) these fonts are basically a must.

`pls` is a pure-Python codebase and is deployed to PyPI. So installing it on any system with a supported Python version is quite straightforward.

```shell
$ python3 -m pip install --user pls
```

There are no native packages _yet_.

## Usage

`pls` has a very simple API with easy to memorise flags. There are no mandatory arguments. Just run `pls` anywhere on your disk.

```shell
$ pls
```

There are a few optional arguments and flags you can use to tweak the behaviour. You can see the complete list of arguments and their description by passing the `--help` or `-h` flags.

```shell
$ pls --help
```

### Directory

The only positional argument is a directory. Pass this to see the contents of a different folder rather than the current working directory.

```shell
$ pls path/to/somewhere/else
```

### Icons

`pls` supports many icons for popular languages out of the box and will show icons by default. If you don't have a Nerd Font (why?), you can switch to emoji icons using `--icons emoji` or `-iemoji`. Be warned they are quite bad. If you are a sad person, you turn icons off using `--icon none` or `-inone`.

**Note:** The built-in icon configuration is intentionally lean. The whole idea is for `pls` to be [customisable by you](pls/data/README.md).

### Filtering

You can choose to hide files or folders from the output using `--no-files` and `--no-dirs` respectively. Passing both will lead to a blank output.

### Sorting

By default `pls` will place all directories first, followed by files with both sorted alphabetically from A to Z. You can prevent folders from being first by passing the `--no-dirs-first` flag. You can change the sort to go from Z to A using `--sort desc` or `-sdesc`. Leading dots are ignored during sorting.

### Alignment

A lot of code related files start with a leading dot `.` for no valid reason. `pls` by default

- lists those files
- moves their name left by one character to line up the actual alphabets
- dims their leading dot

If you don't like this, you can set `--no-align` to turn off all this behaviour in one swoop.

### Details

When you need more infomation about your files, pass the `--details` flag. This expands the list into a table, with

- permissions
- owner name
- size

added to the output. The permissions are presented as `rwx` triplets. The size is presented in binary compound-units (the ones with the "i" like "*iB"). You can switch to decimal units by passing `--units decimal` or `-udecimal`. This flag has no effect unless the `--detail` flag is passed too.
