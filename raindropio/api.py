from __future__ import annotations
from typing import (
    Optional,
    Any,
)

import json
import enum
import datetime

import requests


class API:
    """Provides communication to the Raindrop.io API server.

    :param str token: An access token for authorization.
    """

    _token: str

    def __init__(self, token):
        self._token = token

    def _json_unknown(self, obj: Any) -> Any:
        if isinstance(obj, enum.Enum):
            return obj.value

        if isinstance(obj, datetime.datetime):
            return obj.isoformat()

        raise TypeError(
            f"Object of type {obj.__class__.__name__} " f"is not JSON serializable"
        )

    def _to_json(self, obj: Any) -> Optional[str]:
        if obj is not None:
            return json.dumps(obj, default=self._json_unknown)
        else:
            return None

    def _request_headers(self):
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self._token}",
        }

    def get(self, url, params=None):
        """Send a GET request

        :param url: The url to send request
        :type url: str

        :param params: (optional) Dictionary, list of tuples or bytes to send
            in the query string for the :class:`Request`.

        :return: :class:`requests.Response` object
        :rtype: :class:`requests.Response`
        """

        ret = requests.get(url, headers=self._request_headers(), params=params)
        ret.raise_for_status()
        return ret

    def put(self, url, json=None):
        json = self._to_json(json)
        ret = requests.put(url, headers=self._request_headers(), data=json)
        ret.raise_for_status()
        return ret

    def post(self, url, json=None):
        json = self._to_json(json)
        ret = requests.post(url, headers=self._request_headers(), data=json)
        ret.raise_for_status()
        return ret

    def delete(self, url, json=None):
        json = self._to_json(json)
        ret = requests.delete(url, headers=self._request_headers(), data=json)
        ret.raise_for_status()
        return ret
