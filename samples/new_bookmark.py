import os

from raindropio import *

api = API(os.environ["RAINDROP_TOKEN"])


collection = Collection.create(api, title="Test collection")

raindrop = Raindrop.create(
    api, link="https://www.python.org/", tags=["abc", "def"], collection=collection
)
print(raindrop.title)
