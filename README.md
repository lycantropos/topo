topo
====

[![](https://travis-ci.org/lycantropos/topo.svg?branch=master)](https://travis-ci.org/lycantropos/topo "Travis CI")
[![](https://ci.appveyor.com/api/projects/status/github/lycantropos/topo?branch=master&svg=true)](https://ci.appveyor.com/project/lycantropos/topo "AppVeyor")
[![](https://codecov.io/gh/lycantropos/topo/branch/master/graph/badge.svg)](https://codecov.io/gh/lycantropos/topo "Codecov")
[![](https://img.shields.io/github/license/lycantropos/topo.svg)](https://github.com/lycantropos/topo/blob/master/LICENSE "License")
[![](https://badge.fury.io/py/topo.svg)](https://badge.fury.io/py/topo "PyPI")

In what follows
- `python` is an alias for `python3.5` or any later
version (`python3.6` and so on),
- `pypy` is an alias for `pypy3.5` or any later
version (`pypy3.6` and so on).

Installation
------------

Install the latest `pip` & `setuptools` packages versions:
- with `CPython`
  ```bash
  python -m pip install --upgrade pip setuptools
  ```
- with `PyPy`
  ```bash
  pypy -m pip install --upgrade pip setuptools
  ```

### User

Download and install the latest stable version from `PyPI` repository:
- with `CPython`
  ```bash
  python -m pip install --upgrade topo
  ```
- with `PyPy`
  ```bash
  pypy -m pip install --upgrade topo
  ```

### Developer

Download the latest version from `GitHub` repository
```bash
git clone https://github.com/lycantropos/topo.git
cd topo
```

Install:
- with `CPython`
  ```bash
  python setup.py install
  ```
- with `PyPy`
  ```bash
  pypy setup.py install
  ```

Development
-----------

### Bumping version

#### Preparation

Install
[bump2version](https://github.com/c4urself/bump2version#installation).

#### Pre-release

Choose which version number category to bump following [semver
specification](http://semver.org/).

Test bumping version
```bash
bump2version --dry-run --verbose $CATEGORY
```

where `$CATEGORY` is the target version number category name, possible
values are `patch`/`minor`/`major`.

Bump version
```bash
bump2version --verbose $CATEGORY
```

This will set version to `major.minor.patch-alpha`. 

#### Release

Test bumping version
```bash
bump2version --dry-run --verbose --tag release
```

Bump version
```bash
bump2version --verbose --tag release
```

This will set version to `major.minor.patch` and add `Git` tag.

#### Notes

To avoid inconsistency between branches and pull requests,
bumping version should be merged into `master` branch as separate pull
request.

### Running tests

Plain:
- with `CPython`
  ```bash
  python setup.py test
  ```
- with `PyPy`
  ```bash
  pypy setup.py test
  ```

Inside `Docker` container:
- with `CPython`
  ```bash
  docker-compose --file docker-compose.cpython.yml up
  ```
- with `PyPy`
  ```bash
  docker-compose --file docker-compose.pypy.yml up
  ```

`Bash` script (e.g. can be used in `Git` hooks):
- with `CPython`
  ```bash
  ./run-tests.sh
  ```
  or
  ```bash
  ./run-tests.sh cpython
  ```

- with `PyPy`
  ```bash
  ./run-tests.sh pypy
  ```

`PowerShell` script (e.g. can be used in `Git` hooks):
- with `CPython`
  ```powershell
  .\run-tests.ps1
  ```
  or
  ```powershell
  .\run-tests.ps1 cpython
  ```
- with `PyPy`
  ```powershell
  .\run-tests.ps1 pypy
  ```
