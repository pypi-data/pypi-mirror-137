from __future__ import annotations

from typing import Any
from typing import Iterable, Iterator, Tuple
from typing import TypeVar, Generic

X = TypeVar('X')
Y = TypeVar('Y')


class HttpEngine(object):

    def session(self) -> HttpSession:
        raise NotImplementedError()


class HttpSession(object):

    async def download(self, url: str, filename: str):
        raise NotImplementedError()

    async def request(self, url: str, method='GET', body=None) -> Tuple[Any, Any]:
        raise NotImplementedError()

    async def __aenter__(self):
        raise NotImplementedError()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        raise NotImplementedError()

    async def close(self):
        raise NotImplementedError()


class XmlNode(Iterable['XmlNode']):

    def __iter__(self) -> Iterator[XmlNode]:
        raise NotImplementedError()

    def find_by_css(self, css: str) -> XmlNode:
        raise NotImplementedError()

    def find_by_xpath(self, xpath: str) -> XmlNode:
        raise NotImplementedError()

    def as_text(self) -> str:
        raise NotImplementedError()

    def attr(self, attr) -> Iterable[str]:
        raise NotImplementedError()

    def is_emtpy(self) -> bool:
        raise NotImplementedError()

    def text(self) -> Iterable[str]:
        raise NotImplementedError()


class XmlEngine(object):

    def __call__(self, raw_xml: str) -> XmlNode:
        raise NotImplementedError()


class Context(object):
    xml_engine: XmlEngine
    http_engine: HttpEngine

    async def close(self):
        raise NotImplementedError()

    def resolve_url(self, url: str) -> str:
        raise NotImplementedError()

    async def download(self, url: str, filename: str):
        raise NotImplementedError()

    async def http_request(self, url, method='GET', body=None) -> Tuple[Context, Any]:
        raise NotImplementedError()

    def __iter__(self):
        raise NotImplementedError()


class Collector(Generic[X, Y]):

    async def __call__(self, context: Context, item: X) -> Tuple[Context, Y]:
        raise NotImplementedError()


class Robot(object):

    def __enter__(self) -> 'Robot':
        raise NotImplementedError()

    def __exit__(self, exc_type, exc_val, exc_tb):
        raise NotImplementedError()

    async def run(self, collector: Collector[None, Y]) -> Y:
        raise NotImplementedError()

    def sync_run(self, collector: Collector[None, Y]) -> Y:
        raise NotImplementedError()
