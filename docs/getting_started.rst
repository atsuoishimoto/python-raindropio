

Getting started
=======================



Installation
------------------

You can install latest version from PyPI::

    pip install python-raindropio

You can also get source code from `Github <https://github.com/atsuoishimoto/python-raindropio>`_.


Getting token
----------------------


You need to get a token to use Raindrop.io APIs. 

1. Register your application at `Developers page <https://app.raindrop.io/#/settings/apps/dev>`_.

2. In the application page you created, create the test token to run samples.


Running code
-------------------------

This sample retrieves all bookmarks from *Unsorted* collection.

::

   from raindropio.api import API, CollectionRef, Raindrop
   api = API(YOUR-TEST-TOKEN-HERE)

   page = 0
   while (items:=Raindrop.search(api, collection=CollectionRef.Unsorted, page=page)):
       for item in items:
          print(item.title)
       page += 1


