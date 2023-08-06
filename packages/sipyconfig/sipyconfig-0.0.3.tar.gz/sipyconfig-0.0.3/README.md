# SportIdent Config+ Implementation

A python implementation of the functionality of SPORTident Config+.

Currently only working and tested under Linux.

Note that you might need to add your user to a group that has access to the systems serial interfaces.

## Install

install via pip:
`pip install --upgrade sipyconfig`


## Usage

Create a `SiUSBStation` object using:
```
from sipyconfig import SiUSBStation

si = SiUSBStation()
si.trigger_feedback()
```
have fun :)

## API docs

a part of the api is documented in [Codes.md](docs/Codes.md)
