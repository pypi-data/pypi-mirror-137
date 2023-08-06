# cppgsh  by Python Library
[![Upload pypi.org](https://github.com/kirin123kirin/cppgsh/actions/workflows/pypi.yml/badge.svg?branch=v0.2.1)](https://github.com/kirin123kirin/cppgsh/actions/workflows/pypi.yml)

# Overview
This Program Inspired by [Quom](https://github.com/Viatorus/quom#quom) I made.

# Goal
* Automation Build Single header for C++.

# Implementation
What is different from the original Quom?
* It is automatically looks for the root header or source 
and creates a single header in the proper order.

* Put the include file at the beginning to eliminate duplication.

# Install
```
$ pip install cppgsh
```

# UnInstall
```
$ pip uninstall cppgsh
```

# Requirement
* python3.6 later.

# Liscense
* [MIT Liscense](https://github.com/kirin123kirin/cppgsh/blob/master/LICENSE)

# run command Environment
* Windows
* Linux
* Mac OSX

# Usage
```
usage: cppgsh [-h] [--include_guard format]
              [--include_directory INCLUDE_DIRECTORY]
              [--source_directory SOURCE_DIRECTORY]
              [--exclude_patterns EXCLUDE_PATTERNS]
              [--license_files LICENSE_FILES] [--del_extern_C]
              [--linesep LINESEP] [--encoding ENCODING] [--quiet]
              output

Single header generator for C++ libraries.

positional arguments:
  output                Output file path of the generated single header file.

optional arguments:
  -h, --help            show this help message and exit
  --include_guard format, -g format
                        Regex format of the include guard. Default: None
  --include_directory INCLUDE_DIRECTORY, -I INCLUDE_DIRECTORY
                        Add include directories for header files.
  --source_directory SOURCE_DIRECTORY, -S SOURCE_DIRECTORY
                        Set the source directories for source files. Use ./ or
                        .\ in front of a path to mark as relative to the
                        header file.
  --exclude_patterns EXCLUDE_PATTERNS, -E EXCLUDE_PATTERNS
                        Set the source directories for source files. Use ./ or
                        .\ in front of a path to mark as relative to the
                        header file.
  --license_files LICENSE_FILES, -L LICENSE_FILES
                        Set headline writing License text file path
  --del_extern_C        delete define "extern "C""
  --linesep LINESEP, -l LINESEP
                        line separator of output file.
  --encoding ENCODING, -e ENCODING
                        The encoding used to read and write all files.
  --quiet, -q           no print progress info

```
# Example
TODO

# Libraries used
* [quom](https://pypi.org/project/quom)

