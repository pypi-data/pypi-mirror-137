from __future__ import annotations
from robot.http_engine.aiohttp_engine import AioHttpAdapter
from robot.api import Context, HttpEngine, HttpSession
from dataclasses import dataclass, field
from typing import Tuple, Any, Dict
from urllib.parse import urlparse

import logging
from logging import Logger

__logger__ = logging.getLogger(__name__)


@dataclass()
class ContextImpl(Context):
    http_engine: HttpEngine = field(default_factory=AioHttpAdapter)
    url: Any = None
    http_headers: Dict[str, str] = field(default_factory=dict)
    http_session: HttpSession = None
    logger: Logger = field(default=__logger__)

    def __iter__(self):
        yield 'url', self.url.geturl()
        yield 'headers', dict(self.http_headers)

    def clone(self, **override) -> ContextImpl:
        new_instance = self.__class__(**self.__dict__)
        for k, v in override.items():
            setattr(new_instance, k, v)
        return new_instance

    async def close(self):
        if self.http_session is None:
            return
        await self.http_session.close()
        self.http_session = None

    def get_http_session(self) -> HttpSession:
        if self.http_session is not None:
            return self.http_session
        self.http_session = self.http_engine.session()
        return self.http_session

    def resolve_url(self, url: str):
        if self.url is None:
            return url
        if '://' in url:
            return url
        if url.startswith('//'):
            return self.url.scheme + ':' + url
        if url.startswith('/'):
            return self.url.scheme + '://' + self.url.netloc + url
        base_path, _ = self.url.path.rsplit('/', 1)
        return ''.join([
            self.url.scheme,
            '://',
            self.url.netloc,
            base_path,
            '/',
            url,
        ])

    async def download(self, url: str, filename: str):
        session = self.get_http_session()
        await session.download(url, filename)

    async def http_request(self, url, method = 'GET', body = None) -> Tuple[Context, Any]:
        session = self.get_http_session()
        url = self.resolve_url(url)
        headers, response = await session.request(url, method, body)
        return self.clone(
            url=urlparse(url),
            http_headers=headers,
            http_session=session,
        ), response
