# alias-cd
This tool is meant to help developers create aliases for directories on their local machines. It is configured through a simple yaml file.

![Tests](https://github.com/BenjaminNMitchell/alias-cd/actions/workflows/tests.yml/badge.svg)
![code style](https://img.shields.io/badge/code%20style-black-000000.svg)
![Latest Version](https://pypip.in/version/alias-cd/badge.svg)

## Quick Start
### Install
You can install directly with pip
```bash
pip install alias-cd
```

However we recommend installing with [pipx](https://github.com/pypa/pipx) to keep this tool isolated
```bash
brew install pipx
pipx install alias-cd
```

Copy this [bash function](bin/godir.sh) into your `~/.bash_profile` or `~/.zshrc`

### Configure
The following is an example configuration file. Which you can drop into `~/.config/alias_cd`
```yaml
---
"~":
  # _alias with no value is used as the default directory
  _alias:
  # Used a nested tree structure 
  Documents:
    # Uses _alias tags to set shorter names for directories
    _alias: docs
    repos:
      _alias: repos
      open-source: # Aliases are optional
        my-repo:
          _alias: fun
      public:
        my-organizations-repo:
          _alias: work
```

## Components
### alias-cd
This is a python CLI tool which interacts with the config file

#### Usage
### godir
The primary usecase for this application is to move to a new directory by it's alias. This cannot be done in the python tool. You would need to run the following: `cd $(alias-cd get <alias>)`. For convenience we provide a bash function [godir](bin/godir.sh) which simplifies this and handles errors.

#### Usage
```
godir <alias>
```