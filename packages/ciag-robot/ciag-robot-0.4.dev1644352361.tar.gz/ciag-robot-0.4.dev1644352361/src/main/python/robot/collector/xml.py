import logging
from dataclasses import dataclass, field
from logging import Logger
from typing import Iterable, Tuple

from robot.api import Collector, XmlNode, Context

__logger__ = logging.getLogger(__name__)


@dataclass()
class XPathCollector(Collector[XmlNode, XmlNode]):
    xpath: str
    logger: Logger = field(default=__logger__, compare=False)

    async def __call__(self, context: Context, item: XmlNode) -> Tuple[Context, XmlNode]:
        return context, item.find_by_xpath(self.xpath)


@dataclass()
class AttrCollector(Collector[XmlNode, Iterable[str]]):
    attr: str
    logger: Logger = field(default=__logger__, compare=False)

    async def __call__(self, context: Context, item: XmlNode) -> Tuple[Context, Iterable[str]]:
        return context, [
            value
            for value in item.attr(self.attr)
        ]


@dataclass()
class AsTextCollector(Collector[XmlNode, str]):
    prefix: str = ''
    suffix: str = ''
    logger: Logger = field(default=__logger__, compare=False)

    async def __call__(self, context: Context, item: XmlNode) -> Tuple[Context, str]:
        if item.is_emtpy():
            return context, None
        return context, self.prefix + item.as_text() + self.suffix


@dataclass()
class TextCollector(Collector[XmlNode, Iterable[str]]):
    prefix: str = ''
    suffix: str = ''
    logger: Logger = field(default=__logger__, compare=False)

    async def __call__(self, context: Context, item: XmlNode) -> Tuple[Context, Iterable[str]]:
        return context, [
            self.prefix + value + self.suffix
            for value in item.text()
        ]
