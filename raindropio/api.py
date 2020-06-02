from __future__ import annotations
from typing import Optional, Any, List, Dict, cast, Sequence, ClassVar, TypeVar, Generic, Callable, Tuple, overload, Type, Union
from dataclasses import dataclass
import json
import enum
import datetime
from dateutil.parser import parse as dateparse
import requests
from abc import ABCMeta, abstractmethod


E = TypeVar('E', bound='JSONFriendlyEnum')


class JSONFriendlyEnum(enum.Enum):
    @classmethod
    def json_unknown(cls, value:Any)->Any:
        raise TypeError(
            f'Invalid value for type {cls.__name__}: {value!r}')

    @classmethod
    def fromjson(cls:Type[E], value: Any) -> E:
        try:
            return cls(value)
        except ValueError:
            return cls.json_unknown(value)

    def tojson(self) -> Any:
        return self.value

class AccessLevel(enum.IntEnum, JSONFriendlyEnum):
    readonly = 1
    collaborator_read = 2
    collaborator_write = 3
    owner = 4



class View(JSONFriendlyEnum):
    list = "list"
    simple = "simple"
    grid = "grid"
    masonly = "masonry"




class DictData:
    data: Dict[str, Any]

    def __init__(self, data: Dict[str, Any]) -> None:
        self.data = data

F = TypeVar("F")

Construnctor= Callable[[Any], F]

def optional(f:Construnctor[F])->Callable[[Any], Optional[F]]:
    def wrap(value:Any)->Optional[F]:
        return f(value)
    return wrap


class _Omit(JSONFriendlyEnum):
    omit = True

class Field(Generic[F]):
    ctor : Tuple[Optional[Construnctor[F]]]
    name: Optional[str]


    def __init__(self, ctor:Optional[Construnctor[F]]=None, *, name:Optional[str]=None, default:Any=_Omit.omit):

        self.ctor = (ctor,)
        self.name = name
        self.default = default

    def __set_name__(self, owner: Any, name: str) -> None:
        if self.name is None:
            self.name = name

    def __get__(self, instance: Any, owner: type) -> F:
        if self.name in instance.data:
            value = instance.data[self.name]
            ctor = self.ctor[0]
            if ctor is not None:
                return ctor(value)
            else:
                return cast(F, value)

        if self.default is not _Omit.omit:
            return cast(F, self.default)

        raise ValueError(f"{self.name} is not found")

class CollectionRef(DictData):
    Unsorted: ClassVar[CollectionRef]
    Trash: ClassVar[CollectionRef]

    id = Field[int]()

    
CollectionRef.Unsorted = CollectionRef({"id":-1})
CollectionRef.Trash = CollectionRef({"id":-1})


class UserRef(DictData):
    id = Field[int](name="$id")



class Access(DictData):
    for_ = Field(UserRef, name="for")
    level = Field[int]()
    draggable = Field[bool]()




class Collection(DictData):
    id = Field[int](name="_id")
    access = Field(Access)
    collaborators = Field[Optional[List]](default=None)
    color = Field[Optional[str]](default=None)
    count = Field[int]()
    cover = Field[List[str]]()
    created = Field(dateparse)
    expanded = Field[bool]()
    lastUpdate = Field(dateparse)
    parent = Field[Optional[CollectionRef]](CollectionRef, default=None)
    public = Field[bool]()
    sort = Field[int]()
    title = Field[str]()
    user = Field(UserRef)
    view = Field(View)

    @classmethod
    def get_roots(cls, api: API) -> Sequence[Collection]:
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

        URL = f"https://api.raindrop.io/rest/v1/collection"
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









class RaindropType(JSONFriendlyEnum):
    link = "link"
    article = "article"
    image = "image"
    video = "video"
    document = "document"
    audio = "audi"



#@dataclass
#class Cache:
#    pass
#
#
#@dataclass
#class File:
#    pass


class Raindrop(DictData):
    id = Field[int](name="_id")
    access = Field(Access)
    collaborators = Field[Optional[List]](default=None)
    color = Field[Optional[str]](default=None)
    count = Field[int]()


    id = Field[int](name="_id")
    collection = Field(CollectionRef)
    cover= Field[str]()
    created= Field(dateparse)
    domain= Field[str]()
    excerpt= Field[str]()
    lastUpdate= Field(dateparse)
    link= Field[str]()
    media= Field[Sequence[Dict[str, Any]]]()
    tags= Field[Sequence[str]]()
    title= Field[str]()
    type= Field(RaindropType)
    user= Field(UserRef)

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

        args:Dict[str, Any] = {
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

        URL = f"https://api.raindrop.io/rest/v1/raindrop"
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

        args:Dict[str, Any] = {}
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

        return [cls(item) for item in results['items']]



class API:
    _token: str

    def __init__(self, token):
        self._token = token

    def _json_unknown(self, obj:Any)->Any:
        if isinstance(obj, JSONFriendlyEnum):
            return obj.tojson()

        if isinstance(obj, datetime.datetime):
            return obj.isoformat()

        raise TypeError(f'Object of type {obj.__class__.__name__} '
                        f'is not JSON serializable')

    def _to_json(self, obj:Any)->Optional[str]:
        if obj is not None:
            return json.dumps(obj, default=self._json_unknown)
        else:
            return None

    def _request_headers(self):
        return {
             'Content-Type': 'application/json',
             "Authorization": f"Bearer {self._token}"
            }
            
    def get(self, url, params=None):
        ret = requests.get(
            url, headers=self._request_headers(), params=params
        )
        ret.raise_for_status()
        return ret

    def put(self, url, json=None):
        json=self._to_json(json)
        ret = requests.put(
            url, headers=self._request_headers(), data=json
        )
        ret.raise_for_status()
        return ret

    def post(self, url, json=None):
        json=self._to_json(json)
        ret = requests.post(
            url, headers=self._request_headers(), data=json
        )
        ret.raise_for_status()
        return ret

    def delete(self, url, json=None):
        json=self._to_json(json)
        ret = requests.delete(
            url, headers=self._request_headers(), data=json
        )
        ret.raise_for_status()
        return ret
