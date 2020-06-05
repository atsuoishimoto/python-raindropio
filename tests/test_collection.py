import os
from pprint import pprint
import requests
from raindropio import api

import datetime

from dotenv import load_dotenv  # type: ignore

load_dotenv()

token = os.getenv("RAINDROP_TOKEN")


def test_get():
    for c in api.Collection.get_roots(api.API(token)):
        print("------------------------------")
        print("id", c.id)
        print("access", c.access)
        print("collaborators", c.collaborators)
        print("color", c.color)
        print("count", c.count)
        print("cover", c.cover)
        print("created", c.created)
        print("expanded", c.expanded)
        print("lastUpdate", c.lastUpdate)
        print("parent", c.parent)
        print("public", c.public)
        print("sort", c.sort)
        print("title", c.title)
        print("user", c.user)
        print("view", c.view)

    for c in api.Collection.get_childrens(api.API(token)):
        print(c)

    c = api.Collection.get(api.API(token), c.id)
    print(c)


def test_put():
    title = str(datetime.datetime.now())
    c = api.Collection.update(
        api.API(token), id=11561930, title=title, view=api.View.list
    )
    assert c.title == title


def test_post():
    c = api.Collection.create(api.API(token), title="abcdef")
    assert c.title == "abcdef"

    api.Collection.remove(api.API(token), id=c.id)
