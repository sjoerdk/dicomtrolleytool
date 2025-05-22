# dicomtrolleytool

[![CI](https://github.com/sjoerdk/dicomtrolleytool/actions/workflows/build.yml/badge.svg?branch=main)](https://github.com/sjoerdk/dicomtrolley/actions/workflows/build.yml?query=branch%3Amaster)
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

## Development - Alpha
Nov 2023: This is a personal tool. I try to keep it clean and tested enough to continue developing, but expect 
NotImplementedError, incomplete coverage, incomplete docs, missing parameters. If this tool 
containue to work for me I might make an effort and clean up.



## Installation
```
pip install dicomtrolleytool
``` 

## Setup
NOTE: this whole section is not implemented yet (feel free to step in). The actual
current method of setting up channels is:
* Install keyring (see 'handling credentials' below)
* Look at `/examples/persist_connection`, fill in and run
* Manually edit your settings file `trolley settings edit` to add your channel to 
  the `channels` list.

A `channel` is ready-to use communication channel including password. This needs to be saved to 
a secure location. To this end the channel information is first entered into a file, which is then
stored in a secure location using the `store` command.
```
trolley channel new <type>
# Creates a new empty channel file
# Add data to this file, then:
trolley channel store <template_file>
shred -d <template_file>
```

### Handling credentials
intall [keyring](https://pypi.org/project/keyring/). Works great. 
But installation can be a bit fiddly because it has to link to your OS secret store.
I've only tested this 

For me the magic installation string (tested on on ubuntu 20,22,24) was: 
```
pip install secretstorage dbus-python keyring
```
But this could definitely be just my system.. [Just search for it](https://kagi.com/search?q=python+keyring+install) 

When that works, you need to write your dicomtrolley channels into your secret store
For this, look at `/examples/persist_connection`. Would be great to have a cli command
for this like `trolley credentials add -f <json file>` but there isn't. Feel free to add.

## Usage
You can used the keyword `trolley` from the command line.

Some examples:
```
> trolley query suid 12345                     # simple query
> trolley query suid 12345 324345 345345       # query multiple
> trolley query patient_id 1234
> trolley download suid 12345


```
## Query levels
You can get series level information like this:
```
> trolley query suid 123 --query-level Series
```

## Filtering output
You can restrict the output using --output-fields
```
> trolley -v query acc 1234 --query-level INSTANCE --output-format TABLE --output-fields ProtocolName,SeriesInstanceUID,PatientID

```