# python-raindropio

Python wrapper for [Raindrop.io API](https://developer.raindrop.io/).

This library is in the early stage of development.

## Requirements


- Requires Python 3.7 or later.


## Install

pip3 install python-raindropio


## Usage

```python

from raindropio.api import API, CollectionRef, Raindrop
api = API(raidrop-access-token)

while (items:=Raindrop.search(api)):
    for item in items:
        print(item.title)

```


## License

Copyright 2020 Atsuo Ishimoto

See LICENSE for detail.
