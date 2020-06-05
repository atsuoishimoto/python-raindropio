from __future__ import annotations
from typing import (
    Optional,
    Any,
    List,
    Dict,
    Sequence,
    ClassVar,
    Union,
)

import json
import enum
import datetime

from dateutil.parser import parse as dateparse
from jashin.dictattr import DictModel, DictAttr, DictAttrList

from .api import API

__all__ = [
    "Access",
    "AccessLevel",
    "BrokenLevel",
    "Collection",
    "CollectionRef",
    "DictModel",
    "FontColor",
    "Group",
    "Raindrop",
    "RaindropType",
    "User",
    "UserConfig",
    "UserFiles",
    "UserRef",
    "View",
]


class AccessLevel(enum.IntEnum):
    readonly = 1
    collaborator_read = 2
    collaborator_write = 3
    owner = 4


class View(enum.Enum):
    list = "list"
    simple = "simple"
    grid = "grid"
    masonly = "masonry"


class CollectionRef(DictModel):
    Unsorted: ClassVar[CollectionRef]
    Trash: ClassVar[CollectionRef]

    id = DictAttr[int](name="$id")


CollectionRef.Unsorted = CollectionRef({"$id": -1})
CollectionRef.Trash = CollectionRef({"$id": -1})


class UserRef(DictModel):
    """Represents reference to :class:`User` object. """

    #: (:class:`int`) The id of the :class:`User`.
    id = DictAttr[int](name="$id")


class Access(DictModel):
    """Represents Access control of Collections"""

    #: (:class:`UserRef`) The user for this permission.
    level = DictAttr(AccessLevel)

    #: (:class:`bool`) True if possible to change parent.
    draggable = DictAttr[bool]()


class Collection(DictModel):
    """Represents Collection"""

    #: (:class:`int`) The id of the collection.
    id = DictAttr[int](name="_id")

    #: (:class:`Access`) Permissions for this collection
    access = DictAttr(Access)

    collaborators = DictAttr[Optional[List]](default=None)
    color = DictAttr[Optional[str]](default=None)
    count = DictAttr[int]()
    cover = DictAttr[List[str]]()
    created = DictAttr(dateparse)
    expanded = DictAttr[bool]()
    lastUpdate = DictAttr(dateparse)
    parent = DictAttr[Optional[CollectionRef]](CollectionRef, default=None)
    public = DictAttr[bool]()
    sort = DictAttr[int]()
    title = DictAttr[str]()
    user = DictAttr(UserRef)
    view = DictAttr(View)

    @classmethod
    def get_roots(cls, api: API) -> Sequence[Collection]:
        """Get root collections"""
        URL = "https://api.raindrop.io/rest/v1/collections"
        ret = api.get(URL)
        items = ret.json()["items"]
        return [cls(item) for item in items]

    @classmethod
    def get_childrens(cls, api: API) -> Sequence[Collection]:
        URL = "https://api.raindrop.io/rest/v1/collections/childrens"
        ret = api.get(URL)
        items = ret.json()["items"]
        return [cls(item) for item in items]

    @classmethod
    def get(cls, api: API, id: int) -> Collection:
        URL = f"https://api.raindrop.io/rest/v1/collection/{id}"
        item = api.get(URL).json()["item"]
        return cls(item)

    @classmethod
    def create(
        cls,
        api: API,
        view: Optional[View] = None,
        title: Optional[str] = None,
        sort: Optional[int] = None,
        public: Optional[bool] = None,
        parent: Optional[int] = None,
        cover: Optional[Sequence[str]] = None,
    ) -> Collection:

        args: Dict[str, Any] = {}
        if view is not None:
            args["view"] = view
        if title is not None:
            args["title"] = title
        if sort is not None:
            args["sort"] = sort
        if public is not None:
            args["public"] = public
        if parent is not None:
            args["parent"] = parent
        if cover is not None:
            args["cover"] = cover

        URL = "https://api.raindrop.io/rest/v1/collection"
        item = api.post(URL, json=args).json()["item"]
        return Collection(item)

    @classmethod
    def update(
        cls,
        api: API,
        id: int,
        expanded: Optional[bool] = None,
        view: Optional[View] = None,
        title: Optional[str] = None,
        sort: Optional[int] = None,
        public: Optional[bool] = None,
        parent: Optional[int] = None,
        cover: Optional[Sequence[str]] = None,
    ) -> Collection:

        args: Dict[str, Any] = {}
        if expanded is not None:
            args["expanded"] = expanded
        if view is not None:
            args["view"] = view
        if title is not None:
            args["title"] = title
        if sort is not None:
            args["sort"] = sort
        if public is not None:
            args["public"] = public
        if parent is not None:
            args["parent"] = parent
        if cover is not None:
            args["cover"] = cover

        URL = f"https://api.raindrop.io/rest/v1/collection/{id}"
        item = api.put(URL, json=args).json()["item"]
        return Collection(item)

    @classmethod
    def remove(cls, api: API, id: int):
        URL = f"https://api.raindrop.io/rest/v1/collection/{id}"
        api.delete(URL, json={})


class RaindropType(enum.Enum):
    link = "link"
    article = "article"
    image = "image"
    video = "video"
    document = "document"
    audio = "audi"


class Raindrop(DictModel):
    """Raindrop"""

    id = DictAttr[int](name="_id")
    collection = DictAttr(CollectionRef)
    cover = DictAttr[str]()
    created = DictAttr(dateparse)
    domain = DictAttr[str]()
    excerpt = DictAttr[str]()
    lastUpdate = DictAttr(dateparse)
    link = DictAttr[str]()
    media = DictAttr[Sequence[Dict[str, Any]]]()
    tags = DictAttr[Sequence[str]]()
    title = DictAttr[str]()
    type = DictAttr(RaindropType)
    user = DictAttr(UserRef)

    #    broken: bool
    #    cache: Cache
    #    creatorRef: UserRef
    #    file: File
    #    important: bool
    #    html: str

    @classmethod
    def get(cls, api: API, id: int) -> Raindrop:
        URL = f"https://api.raindrop.io/rest/v1/raindrop/{id}"
        item = api.get(URL).json()["item"]
        return cls(item)

    @classmethod
    def create(
        cls,
        api: API,
        link: str,
        pleaseParse: bool = True,
        created: Optional[datetime.datetime] = None,
        lastUpdate: Optional[datetime.datetime] = None,
        order: Optional[int] = None,
        important: Optional[bool] = None,
        tags: Optional[Sequence[str]] = None,
        media: Optional[Sequence[Dict[str, Any]]] = None,
        cover: Optional[str] = None,
        collection: Optional[Union[Collection, CollectionRef, int]] = None,
        type: Optional[str] = None,
        html: Optional[str] = None,
        excerpt: Optional[str] = None,
        title: Optional[str] = None,
    ) -> Raindrop:

        args: Dict[str, Any] = {
            "link": link,
        }
        if pleaseParse:
            args["pleaseParse"] = {}
        if created is not None:
            args["created"] = created
        if lastUpdate is not None:
            args["lastUpdate"] = lastUpdate
        if order is not None:
            args["order"] = order
        if important is not None:
            args["important"] = important
        if tags is not None:
            args["tags"] = tags
        if media is not None:
            args["media"] = media
        if cover is not None:
            args["cover"] = cover
        if collection is not None:
            if isinstance(collection, (Collection, CollectionRef)):
                args["collection"] = collection.id
            else:
                args["collection"] = collection
        if type is not None:
            args["type"] = type
        if html is not None:
            args["html"] = html
        if excerpt is not None:
            args["excerpt"] = excerpt
        if title is not None:
            args["title"] = title

        URL = "https://api.raindrop.io/rest/v1/raindrop"
        item = api.post(URL, json=args).json()["item"]
        return cls(item)

    @classmethod
    def update(
        cls,
        api: API,
        id: int,
        pleaseParse: Optional[bool] = False,
        created: Optional[datetime.datetime] = None,
        lastUpdate: Optional[datetime.datetime] = None,
        order: Optional[int] = None,
        important: Optional[bool] = None,
        tags: Optional[Sequence[str]] = None,
        media: Optional[Sequence[Dict[str, Any]]] = None,
        cover: Optional[str] = None,
        collection: Optional[Union[Collection, CollectionRef, int]] = None,
        type: Optional[str] = None,
        html: Optional[str] = None,
        excerpt: Optional[str] = None,
        title: Optional[str] = None,
        link: Optional[str] = None,
    ) -> Raindrop:

        args: Dict[str, Any] = {}
        if pleaseParse:
            args["pleaseParse"] = {}
        if created is not None:
            args["created"] = created
        if lastUpdate is not None:
            args["lastUpdate"] = lastUpdate
        if order is not None:
            args["order"] = order
        if important is not None:
            args["important"] = important
        if tags is not None:
            args["tags"] = tags
        if media is not None:
            args["media"] = media
        if cover is not None:
            args["cover"] = cover
        if collection is not None:
            if isinstance(collection, (Collection, CollectionRef)):
                args["collection"] = collection.id
            else:
                args["collection"] = collection
        if type is not None:
            args["type"] = type
        if html is not None:
            args["html"] = html
        if excerpt is not None:
            args["excerpt"] = excerpt
        if title is not None:
            args["title"] = title
        if link is not None:
            args["link"] = link

        URL = f"https://api.raindrop.io/rest/v1/raindrop/{id}"
        item = api.put(URL, json=args).json()["item"]
        return cls(item)

    @classmethod
    def remove(cls, api: API, id: int):
        URL = f"https://api.raindrop.io/rest/v1/raindrop/{id}"
        api.delete(URL, json={})

    @classmethod
    def search(
        cls,
        api: API,
        collection: CollectionRef = CollectionRef.Unsorted,
        page: int = 0,
        perpage: int = 50,
        word: Optional[str] = None,
        tag: Optional[str] = None,
        important: Optional[bool] = None,
    ):

        args: List[Dict[str, Any]] = []
        if word is not None:
            args.append({"key": "word", "val": word})
        if tag is not None:
            args.append({"key": "tag", "val": tag})
        if important is not None:
            args.append({"key": "important", "val": important})

        params = {"search": json.dumps(args), "perpage": perpage, "page": page}

        URL = f"https://api.raindrop.io/rest/v1/raindrops/{collection.id}"

        results = api.get(URL, params=params).json()
        return [cls(item) for item in results["items"]]


class BrokenLevel(enum.Enum):
    basic = "basic"
    default = "default"
    strict = "strict"
    off = "off"


class FontColor(enum.Enum):
    sunset = "sunset"
    night = "night"


class UserConfig(DictModel):
    broken_level = DictAttr(BrokenLevel)
    font_color = DictAttr[Optional[FontColor]](FontColor, default=None)
    font_size = DictAttr[int]()
    last_collection = DictAttr[int]()
    raindrops_view = DictAttr(View)


class Group(DictModel):
    title = DictAttr[str]()
    hidden = DictAttr[bool]()
    sort = DictAttr[int]()
    collections = DictAttrList[int](name="collections")


class UserFiles(DictModel):
    used = DictAttr[int]()
    size = DictAttr[int]()
    lastCheckPoint = DictAttr(dateparse)


class User(DictModel):
    """User"""

    id = DictAttr[int](name="_id")
    config = DictAttr(UserConfig)
    email = DictAttr[str]()
    email_MD5 = DictAttr[str]()
    files = DictAttr(UserFiles)
    fullName = DictAttr[str]()
    groups = DictAttrList(Group)
    password = DictAttr[bool]()
    pro = DictAttr[bool]()
    registered = DictAttr(dateparse)

    @classmethod
    def get(cls, api: API) -> User:
        URL = "https://api.raindrop.io/rest/v1/user"
        user = api.get(URL).json()["user"]
        return cls(user)
