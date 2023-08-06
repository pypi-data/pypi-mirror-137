# CLSLQ

![img](logo.png)

[![GitHub version](https://badge.fury.io/gh/lovelacelee%2Fclslq.svg)](https://badge.fury.io/gh/lovelacelee%2Fclslq)
[![Documentation Status](https://readthedocs.org/projects/clslq/badge/?version=latest)](https://clslq.readthedocs.io/zh_CN/latest/?badge=latest)
[![PyPI version](https://badge.fury.io/py/clslq.svg)](https://badge.fury.io/py/clslq)
      

[CLSLQ](https://clslq.readthedocs.io/) is a python common use function library and toolsets.

Basically collect some useful functions, classes, expressions in python learning process. Why python `pypi` packages suffixed with *.whl(.wheel)*? Because we are making wheels, one on another.

This project bootstrapped since 2021, the playground in python, first python library and module on the way. 


# [ChangeLog](ChangeLog.md)

* Only support `python3`

# TODO

- [ ] QT widgets collections
- [ ] Cookiecutter intergrated
- [x] Add Notion month report generator.
- [x] Add Notion week report generator.
- [x] SQL database operation wapper api
- [x] Global root log wrapper
- [x] Global config wrapper, parser and flusher

# How-To

Here is for the lost memory:

## Use clslq command toolsets

```
$ pip3 install clslq -U
$ clslq --version
$ clslq --help
```

## Running test cases

```
$ pip3 install pytest pytest-html
$ pip3 install -U -r requirements/dev.txt
$ pip3 install -U -r requirements/prod.txt
$ python3 pytest
```

## Develop environment build 

```
$ python3 setup.py venv init
(clslq-RJvATSUq)$ python3 setup.py doc
```

setup.py help

```
$ python3 setup.py --help
$ python3 setup.py --help-commands
```

build doc
```
$ python3 setup.py doccreate
$ python3 setup.py docbuild
$ python3 setup.py docrun
```

publish project to pypi or local pypi

```
$ python3 setup.py publish
$ python3 setup.py distclean
```

## Install to system or just for specified user

for user

```
python3 install clslq --user
python3 -m clslq.cli --help
```

# Depends

* ExcelSupported: [[Stable]](https://docs.xlwings.org/en/stable/#) Which only compatible with Windows and MacOS
* [openpyxl](https://openpyxl.readthedocs.io/en/stable/) is compatible with Linux too.
* [DEV requirements](requirements/dev.txt)
* [PROD requirements](requirements/prod.txt)