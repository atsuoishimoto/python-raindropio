import os
from pprint import pprint
import requests
from raindropio import api
import datetime

from dotenv import load_dotenv
load_dotenv()

token = os.getenv("RAINDROP_TOKEN")


def test_get():
    for c in api.Collection.get_roots(api.API(token)):
        print(c)
    for c in api.Collection.get_childrens(api.API(token)):
        print(c)

    c = api.Collection.get(api.API(token), c.id)
    print(c)


def test_put():
    title = str(datetime.datetime.now())
    c = api.Collection.update(api.API(token), id=11561930, title=title)
    assert c.title == title


def test_post():
    c = api.Collection.create(api.API(token), title="abcdef")
    assert c.title == "abcdef"

    api.Collection.remove(api.API(token), id=c.id)
