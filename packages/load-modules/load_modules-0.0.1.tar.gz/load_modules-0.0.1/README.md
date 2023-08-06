###

# py_load_modules

## Description

py_load_modules is a python3 library which takes a class, and a list of
directories.  It will search within those directories (without any recursive
searching) for classes which implement the argument class. It will return a
list of instances of those classes for use.

## Installation

```
python3 -m pip install  git+https://github.com/rhhayward/py_load_modules.git@master
```

## Usage

Assuming a directory structure like this:

```
from load_modules import load_modules

modules = load_modules.load(SuperClass, ['/path/to/py_files/', 'relative_path/to/py_files'])
for module in modules:
    module.class_method()
```
