import logging
import json
from dataclasses import dataclass, field
from logging import Logger
from typing import Any, Callable, Generic, Iterable, Iterator, Sequence, Tuple, TypeVar
from robot import xml_engine

from robot.api import XmlEngine, XmlNode
from robot.xml_engine.pyquery_engine import PyQueryAdapter

T = TypeVar('T')


class HttpParser(Generic[T]):

    def accept(self, content_type: str) -> Callable[[str], T]:
        raise NotImplementedError()


@dataclass
class HttpParserChain(HttpParser[Any]):

    parsers: Sequence[HttpParser] = field(default_factory=list)

    def accept(self, content_type: str) -> Callable[[str], T]:
        for parser in self.parsers:
            fn = parser.accept(content_type)
            if fn is not None:
                return fn
        return lambda it: it

    @classmethod
    def default(cls):
        return cls((
            JsonParser(),
            XmlParser(),
        ))


@dataclass
class XmlParser(HttpParser[XmlNode]):

    xml_engine: XmlEngine = field(default_factory=PyQueryAdapter)

    def accept(self, content_type: str) -> Callable[[str], XmlNode]:
        if 'application/xml' in content_type:
            return self.xml_engine
        if 'text/html' in content_type:
            return self.xml_engine
        if '+xml' in content_type:
            return self.xml_engine
        return None

    def parse(self, content_type: str, data: str) -> XmlNode:
        return self.xml_engine(data)


class JsonParser(HttpParser[Any]):

    def accept(self, content_type: str) -> bool:
        if 'application/json' in content_type:
            return json.loads
        return None
