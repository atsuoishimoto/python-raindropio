from raindropio.api import API, CollectionRef, Raindrop
import os

api = API(os.environ['RAINDROP_TOKEN'])

page=0
while (items:=Raindrop.search(api, page=page)):
    for item in items:
        print(item.title)
    page += 1
