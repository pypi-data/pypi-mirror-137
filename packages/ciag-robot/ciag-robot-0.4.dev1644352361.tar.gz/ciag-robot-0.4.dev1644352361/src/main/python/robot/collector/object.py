from __future__ import annotations

import logging
from dataclasses import dataclass, field
from logging import Logger
from typing import Dict, Callable, Any, Tuple

from robot.api import Collector, X, Y, Context
from robot.collector.core import DictCollector

__logger__ = logging.getLogger(__name__)


class Object(object):

    @classmethod
    def from_dict(cls, data: Dict) -> Object:
        return cls(dict([
            (k, v if not isinstance(v, dict) else cls.from_dict(v))
            for k, v in data.items()
        ]))

    def __init__(self, attributes):
        self.__dict__.update(attributes)

    def __eq__(self, other):
        if other is None:
            return False
        return self.__dict__ == other.__dict__

    def __repr__(self):
        return f'{self.__class__.__name__}({self.__dict__})'

    def __getitem__(self, item):
        return self.__dict__.__getitem__(item)

    def __setitem__(self, key, value):
        return self.__dict__.__setitem__(key, value)

    def __iter__(self):
        return self.__dict__.__iter__()


@dataclass()
class ObjectCollector(Collector[X, Y]):
    dict_collector: DictCollector[X]
    cast: Callable[[Dict[str, Any]], Y] = field(default=Object.from_dict)
    logger: Logger = field(default=__logger__, compare=False)

    async def __call__(self, context: Context, item: X) -> Tuple[Context, Y]:
        context, value = await self.dict_collector(context, item)
        result = self.cast(value)
        return context, result
