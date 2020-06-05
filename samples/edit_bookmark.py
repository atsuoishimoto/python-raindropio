import os
from raindropio import *

api = API(os.environ["RAINDROP_TOKEN"])

c = Raindrop.create(api, link="https://www.python.org/")
print(c.title, c.link)

c = Raindrop.update(api, id=c.id, title="title")
print(c.title)

Raindrop.remove(api, id=c.id)
