# fdpy

Crude Python port of [fd](https://github.com/sharkdp/fd).

## Requirements
- [fd](https://github.com/sharkdp/fd)
- [python>=3.6](https://www.python.org/downloads/)

## Installation

First, install `fd` (see [sharkdp/fd#installation](https://github.com/sharkdp/fd#installation) for instructions). Then install the package with

```
pip install fdpy
```

❗ **IMPORTANT: `fd` must be in your `$PATH`**

## Usage

```py
>>> from fdpy.fd import FD
>>> fd = FD()
>>> fd.find('foo.txt')
# ['/path/to/cwd/foo.txt', '/path/to/cwd/foo.jpg']
>>> fd.find('Foo.txt', path='/some/dir', hidden=True, no_ignore=True, case_sensitive=True)
# ['/some/dir/Foo.txt', '/some/dir/.Foo']
```
