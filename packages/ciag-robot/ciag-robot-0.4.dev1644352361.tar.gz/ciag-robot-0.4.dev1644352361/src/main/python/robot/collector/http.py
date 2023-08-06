from __future__ import annotations

import logging
from dataclasses import dataclass, field
from logging import Logger
from typing import Any

from robot.api import Collector, Context, XmlNode, Tuple

__logger__ = logging.getLogger(__name__)


@dataclass()
class GetCollector(Collector[str, XmlNode]):
    method: str = 'GET'
    logger: Logger = field(default=__logger__, compare=False)

    async def __call__(self, context: Context, item: str) -> Tuple[Context, XmlNode]:
        sub_context, sub_item = await context.http_request(item, self.method)
        return sub_context, sub_item


@dataclass()
class UrlCollector(Collector[str, str]):
    logger: Logger = field(default=__logger__, compare=False)

    async def __call__(self, context: Context, item: str) -> Tuple[Context, str]:
        return context, context.resolve_url(item)

@dataclass()
class RequestCollector(Collector[Any, Any]):
    url : Collector[Any, str]
    method: str = 'POST'
    logger: Logger = field(default=__logger__, compare=False)

    async def __call__(self, context: Context, item: Any) -> Tuple[Context, XmlNode]:
        url = await self.url(context, item)
        sub_context, sub_item = await context.http_request(url, self.method, item)
        return sub_context, sub_item