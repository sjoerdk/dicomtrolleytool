# dicomtrolleytool

[![CI](https://github.com/sjoerdk/dicomtrolleytool/actions/workflows/build.yml/badge.svg?branch=master)](https://github.com/sjoerdk/dicomtrolley/actions/workflows/build.yml?query=branch%3Amaster)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/dicomtrolleytool)](https://pypi.org/project/dicomtrolleytool/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)

Command line tool to query and retrieve DICOM datasets  

* CLI frontend to [dicomtrolley](https://github.com/sjoerdk/dicomtrolley)
* Developed for debug and testing. Quick queries and downloads from command line
* Convenient handling of login secrets using [keyring](https://pypi.org/project/keyring/)

## Why?
For testing and debugging DICOM server connections I kept creating single use, throw-away python 
scripts. This is annoying for three reasons:
 * Duplication: Copy-pasting code for each single query, files piling up.
 * Slowness: Creating a pyton file, running this is overhead each time.
 * Credential faff: Finding the right credentials and safely including them in this script for each single query.

dicomtrolleytool solves these three issues.

## Installation
```
pip install dicomtrolleytool
``` 

## Usage
From command line:
```
> trolley query StudyInstanceUID=12345

```

## Handling credentials
Add credentials to keyring:
trolley credentials add -f <json file>