# python-raindropio

Python wrapper for [Raindrop.io API](https://developer.raindrop.io/).

This library is in the early stage of development.

## Requirements


- Requires Python 3.7 or later.


## Install

pip3 install python-raindropio


## Usage

You must register your application at https://app.raindrop.io/settings/integrations.
In the application page, create test token to run following samples.

* Create collection

```python

from raindropio import API, Collection
api = API(raidrop_access_token)

c = Collection.create(api, title="Sample collection")
print(c.title)
```


* Search bookmarks from Unsorted collection.

```python

from raindropio import API, CollectionRef, Raindrop
api = API(raidrop_access_token)

page = 0
while (items:=Raindrop.search(api, collection=CollectionRef.Unsorted, page=page)):
    print(page)
    for item in items:
        print(item.title)
    page += 1
```

## License

Copyright 2020 Atsuo Ishimoto

See LICENSE for detail.
