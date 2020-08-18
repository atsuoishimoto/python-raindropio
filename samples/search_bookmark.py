import os

from raindropio import *

api = API(os.environ["RAINDROP_TOKEN"])

page = 0
while (items := Raindrop.search(api, page=page)) :
    for item in items:
        print(item.title, item.excerpt)
    page += 1
