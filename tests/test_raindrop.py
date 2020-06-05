from raindropio import api
import os

from dotenv import load_dotenv  # type: ignore

load_dotenv()

token = os.getenv("RAINDROP_TOKEN")


def test_get():

    c = api.Raindrop.get(api.API(token), 169457551)
    print(c)


def test_create():

    c = api.Raindrop.create(api.API(token), link="https://www.python.org/")
    print(c)

    c = api.Raindrop.create(
        api.API(token),
        link="https://twitter.com/freakboy3742/status/1265194253040316417",
    )

    api.Raindrop.update(api.API(token), id=c.id, title="666666666666&&&&&&&")
    api.Raindrop.remove(api.API(token), id=c.id)


def test_search():

    ret = api.Raindrop.search(api.API(token))
    print(ret)
