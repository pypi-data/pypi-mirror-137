import json
import urllib.parse
from typing import Dict, Optional, Text

import requests
from pydantic import BaseModel

from cnside import errors
from cnside.cli.documents import AnalyzeRequestDoc, AnalyzeResponseDoc
from cnside.objects.encoders import CNSIDEJsonEncoder

__all__ = ["APIClient", "APIClientConfig"]


class APIClientConfig(BaseModel):
    base_url: Text
    headers: Optional[Dict] = {}
    proxies: Optional[Dict] = {}


class APIClient:
    def __init__(self, config: APIClientConfig):
        self.config = config
        self.session = self.open()

        self._analyze_url = urllib.parse.urljoin(self.config.base_url, "analyze")

    def open(self) -> requests.Session:
        s = requests.Session()
        s.headers.update(self.config.headers)
        s.proxies.update(self.config.proxies)
        return s

    def close(self):
        self.session.close()

    def post_analyze_request(self, request_document: AnalyzeRequestDoc) -> AnalyzeResponseDoc:
        response = self.session.post(url=self._analyze_url,
                                     json=json.loads(json.dumps(request_document, cls=CNSIDEJsonEncoder)))

        if response.status_code == 401:
            raise errors.api.TokenExpired()
        elif not response.status_code == 202:
            raise errors.api.RemoteServerError(data=errors.api.ServerErrorData(status_code=response.status_code))

        data = AnalyzeResponseDoc(**response.json())

        return data

    def get_analyze_status(self, workflow_id: Text) -> AnalyzeResponseDoc:
        response = self.session.get(url=f"{self._analyze_url}/{workflow_id}")
        if response.status_code == 404:
            # This is a workaround for some bug in servers side that returns a 404 status code from an unknown reason.
            data = None
        else:
            data = AnalyzeResponseDoc(**response.json())

        return data
