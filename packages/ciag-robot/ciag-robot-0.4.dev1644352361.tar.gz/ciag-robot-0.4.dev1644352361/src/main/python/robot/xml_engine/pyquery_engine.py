from __future__ import annotations

import logging
from dataclasses import dataclass, field
from logging import Logger
from typing import Iterator, Iterable

from pyquery import PyQuery

from robot.api import XmlEngine, XmlNode

__logger__ = logging.getLogger(__name__)


@dataclass()
class PyQueryNodeAdapter(XmlNode):
    engine: PyQueryAdapter = field(compare=False)
    content: PyQuery
    logger: Logger = field(default=__logger__, compare=False)

    def __init__(self, engine: PyQueryAdapter, content: PyQuery):
        self.engine = engine
        self.content = content

    def __iter__(self) -> Iterator[PyQueryNodeAdapter]:
        return self._map(self.content)

    def _map(self, pyquery: PyQuery) -> Iterator[PyQueryNodeAdapter]:
        for item in pyquery:
            yield PyQueryNodeAdapter(self.engine, self.engine.pyquery(item))

    def find_by_css(self, css: str) -> XmlNode:
        return PyQueryNodeAdapter(self.engine, self.content.find(css))

    def find_by_xpath(self, xpath: str) -> XmlNode:
        return PyQueryNodeAdapter(self.engine, self.engine.pyquery(self.content.root.xpath(xpath)))

    def as_text(self) -> str:
        try:
            return self.content.text()
        except AttributeError:
            return ''.join([str(it) for it in self.content])

    def text(self) -> Iterable[str]:
        for item in self:
            yield item.content.text()

    def attr(self, attr: str) -> Iterable[str]:
        for item in self:
            yield item.content.attr(attr)

    def is_emtpy(self) -> bool:
        return len(self.content) == 0

    def __repr__(self):
        return f'{self.__class__.__name__}{{ {self.content} }}'

    def __str__(self):
        return f'{self.__class__.__name__}{{ {self.content} }}'


@dataclass()
class PyQueryAdapter(XmlEngine):
    pyquery: PyQuery = field(default=PyQuery, compare=False)
    logger: Logger = field(default=__logger__, compare=False)

    def __call__(self, raw_xml: str) -> PyQueryNodeAdapter:
        return PyQueryNodeAdapter(self, self.pyquery(raw_xml))
