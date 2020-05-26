from __future__ import annotations
from typing import Optional, Any, List, Dict, cast, Sequence, ClassVar
from dataclasses import dataclass
import json
import enum
import datetime
from dateutil.parser import parse as dateparse
import requests


def _enum_fromjson(cls: Any, value):
    try:
        ret = cls(value)
    except ValueError:
        return cls.unknown


class AccessLevel(enum.IntEnum):
    readonly = 1
    collaborator_read = 2
    collaborator_write = 3
    owner = 4
    unknown = -1

    @classmethod
    def fromjson(cls, value: Any) -> AccessLevel:
        return cast(AccessLevel, _enum_fromjson(cls, value))


class View(enum.Enum):
    list = "list"
    simple = "simple"
    grid = "grid"
    masonly = "masonry"
    unknown = ""

    @classmethod
    def fromjson(cls, value: Any) -> View:
        return cast(View, _enum_fromjson(cls, value))


@dataclass
class UserRef:
    id: int

    @classmethod
    def fromjson(cls, value: Any) -> UserRef:
        return cls(id=cast(int, value["$id"]))


@dataclass
class Access:
    for_: UserRef
    level: int
    draggable: bool

    @classmethod
    def fromjson(cls, value: Any) -> Access:
        return cls(
            for_=UserRef(id=value["for"]),
            level=value["level"],
            draggable=value["draggable"],
        )


@dataclass
class CollectionRef:
    Unsorted: ClassVar[CollectionRef]
    Trash: ClassVar[CollectionRef]
    id: int

    @classmethod
    def fromjson(cls, value: Any) -> CollectionRef:
        return CollectionRef(id=cast(int, value["$id"]))


CollectionRef.Unsorted = CollectionRef(id=-1)
CollectionRef.Trash = CollectionRef(id=-99)


@dataclass
class Collection:
    id: int
    access: Access
    collaborators: Any
    color: Optional[str]
    count: int
    cover: List[str]
    created: datetime.datetime
    expanded: bool
    lastUpdate: datetime.datetime
    parent: Optional[CollectionRef]
    public: bool
    sort: int
    title: str
    user: UserRef
    view: View

    _json: Dict[str, Any]

    @classmethod
    def fromjson(cls, json: Dict[str, Any]) -> Collection:

        parent_ref: Optional[CollectionRef] = None

        parent = json.get("parent")
        if parent:
            parent_ref = CollectionRef.fromjson(parent)

        return cls(
            id=json["_id"],
            access=Access.fromjson(json.get("access")),
            collaborators=json.get("collaborators", {}),
            color=json.get("color", None),
            count=json["count"],
            cover=json["cover"],
            created=dateparse(json["created"]),
            expanded=json["expanded"],
            lastUpdate=dateparse(json["lastUpdate"]),
            parent=parent_ref,
            public=json["public"],
            sort=json["sort"],
            title=json["title"],
            user=UserRef.fromjson(json["user"]),
            view=View.fromjson(json["view"]),
            _json=json,
        )

    @classmethod
    def get_roots(cls, api: API) -> Sequence[Collection]:
        URL = "https://api.raindrop.io/rest/v1/collections"
        ret = api.get(URL)
        items = ret.json()["items"]
        return [cls.fromjson(item) for item in items]

    @classmethod
    def get_childrens(cls, api: API) -> Sequence[Collection]:
        URL = "https://api.raindrop.io/rest/v1/collections/childrens"
        ret = api.get(URL)
        items = ret.json()["items"]
        return [cls.fromjson(item) for item in items]

    @classmethod
    def get(cls, api: API, id: int) -> Collection:
        URL = f"https://api.raindrop.io/rest/v1/collection/{id}"
        item = api.get(URL).json()["item"]
        return cls.fromjson(item)

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

        URL = f"https://api.raindrop.io/rest/v1/collection"
        item = api.post(URL, json=args).json()["item"]
        return Collection.fromjson(item)

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
        return Collection.fromjson(item)

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

    unknown = ""

    @classmethod
    def fromjson(cls, value: Any) -> RaindropType:
        return cast(RaindropType, _enum_fromjson(cls, value))


@dataclass
class Cache:
    pass


@dataclass
class File:
    pass


@dataclass
class Raindrop:
    id: int
    collection: CollectionRef
    cover: str
    created: datetime.datetime
    domain: str
    excerpt: str
    lastUpdate: datetime.datetime
    link: str
    media: Sequence[Dict[str, Any]]
    tags: Sequence[str]
    title: str
    type: RaindropType
    user: UserRef

    #    broken: bool
    #    cache: Cache
    #    creatorRef: UserRef
    #    file: File
    #    important: bool
    #    html: str
    _json: Dict[str, Any]

    @classmethod
    def fromjson(cls, json: Dict[str, Any]) -> Raindrop:
        return cls(
            id=json["_id"],
            collection=CollectionRef.fromjson(json.get("collection")),
            cover=json["cover"],
            created=dateparse(json["created"]),
            domain=json["domain"],
            excerpt=json["excerpt"],
            lastUpdate=dateparse(json["lastUpdate"]),
            link=json["link"],
            media=json["media"],
            tags=json["tags"],
            title=json["title"],
            type=RaindropType.fromjson(json["type"]),
            user=UserRef.fromjson(json["user"]),
            _json=json,
        )

    @classmethod
    def get(cls, api: API, id: int) -> Raindrop:
        URL = f"https://api.raindrop.io/rest/v1/raindrop/{id}"
        item = api.get(URL).json()["item"]
        return cls.fromjson(item)

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
        collection: Optional[CollectionRef] = None,
        type: Optional[str] = None,
        html: Optional[str] = None,
        excerpt: Optional[str] = None,
        title: Optional[str] = None,
    ) -> Raindrop:

        args:Dict[str, Any] = {
            "link": link,
        }
        if pleaseParse:
            args["pleaseParse"] = {}
        if created is not None:
            args["created"] = created.isoformat()
        if lastUpdate is not None:
            args["lastUpdate"] = lastUpdate.isoformat()
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
            args["collection"] = collection.id
        if type is not None:
            args["type"] = type
        if html is not None:
            args["html"] = html
        if excerpt is not None:
            args["excerpt"] = excerpt
        if title is not None:
            args["title"] = title

        URL = f"https://api.raindrop.io/rest/v1/raindrop"
        item = api.post(URL, json=args).json()["item"]
        return cls.fromjson(item)

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
        collection: Optional[CollectionRef] = None,
        type: Optional[str] = None,
        html: Optional[str] = None,
        excerpt: Optional[str] = None,
        title: Optional[str] = None,
        link: Optional[str] = None,
    ) -> Raindrop:

        args:Dict[str, Any] = {}
        if pleaseParse:
            args["pleaseParse"] = {}
        if created is not None:
            args["created"] = created.isoformat()
        if lastUpdate is not None:
            args["lastUpdate"] = lastUpdate.isoformat()
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
            args["collection"] = collection.id
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
        return cls.fromjson(item)

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

        args:List[Dict[str, Any]] = []
        if word is not None:
            args.append({"key": "word", "val": word})
        if tag is not None:
            args.append({"key": "tag", "val": tag})
        if important is not None:
            args.append({"key": "important", "val": important})

        params = {"search": json.dumps(args), "perpage": perpage, "page": page}

        URL = f"https://api.raindrop.io/rest/v1/raindrops/{collection.id}"

        results = api.get(URL, params=params).json()

        return [cls.fromjson(item) for item in results['items']]
            

class API:
    _token: str

    def __init__(self, token):
        self._token = token

    def get(self, url, params=None):
        ret = requests.get(
            url, headers={"Authorization": f"Bearer {self._token}"}, params=params
        )
        ret.raise_for_status()
        return ret

    def put(self, url, json):
        ret = requests.put(
            url, headers={"Authorization": f"Bearer {self._token}"}, json=json
        )
        ret.raise_for_status()
        return ret

    def post(self, url, json):
        ret = requests.post(
            url, headers={"Authorization": f"Bearer {self._token}"}, json=json
        )
        ret.raise_for_status()
        return ret

    def delete(self, url, json):
        ret = requests.delete(
            url, headers={"Authorization": f"Bearer {self._token}"}, json=json
        )
        ret.raise_for_status()
        return ret
