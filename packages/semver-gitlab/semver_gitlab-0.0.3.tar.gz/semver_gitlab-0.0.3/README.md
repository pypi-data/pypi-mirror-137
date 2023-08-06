### Before you begin, ensure that:

- python3 and pip3 are installed
- below packages are up-to-date
    - pip
    - build
    - twine

``` shell
python3 -m pip install --upgrade pip
python3 -m pip install --upgrade build
python3 -m pip install --upgrade twine
```

- *<project_dir>/requirements.txt* dependencies are installed

``` shell
pip install -r requirements.txt
```

---

### How to Run

#### Locally

``` shell
cd src
# Test library
python -m semver_gitlab -b develop -p 33461475 --token="glpat-xFYe3UqanN3SUsH4BbHT"
```

#### Docker

``` shell
# Build
docker build -t semver .

# Get into docker image
docker run -it semver bin/sh
python -m semver_gitlab -b develop -p 33461475 --token="glpat-xFYe3UqanN3SUsH4BbHT"
```

### How to unittest
Develop/build/install locally and then run tests
``` shell
python -m unittest
```

---

### How to Build / Manual Test / Publish

* Create a build
    * dist / *
    * src/<module_name>.egg-info

``` shell
python3 -m build
```

``` shell
# Directory Tree
├───dist
├───src
│   ├───semver_gitlab
│   └───semver_gitlab.egg-info
└───tests

```

* <u>*Install package locally and test it before pushing to a pip repository.*</u>

``` shell
pip install ./dist/<name>-<version>.tar.gz
```

* Push to testpypi (*TEST*)

``` shell
python3 -m twine upload --repository testpypi dist/*
```

* Push to pypi (*PRODUCTION*)

``` shell
python3 -m twine upload dist/*
```

---

### How to Install This Library and Use It

``` shell
# Install dependencies and our library
pip install -r requirements.txt
pip install -i https://test.pypi.org/simple/ semver-gitlab-dfx-test==0.0.3

# Test library
python -m semver_gitlab -b develop -p 33461475 --token="glpat-xFYe3UqanN3SUsH4BbHT"
```

### Library Urls

Production = https://pypi.org/project/semver-gitlab/

Test = https://pypi.org/project/semver-gitlab-dfx-test/