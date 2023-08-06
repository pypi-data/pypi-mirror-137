import logging
from dataclasses import dataclass, field
from itertools import chain
from logging import Logger
from typing import Iterable, List, Callable, Tuple

from robot.api import Collector, X, Context

__logger__ = logging.getLogger(__name__)


@dataclass()
class FlatCollector(Collector[Iterable[Iterable[X]], List[X]]):
    logger: Logger = field(default=__logger__, compare=False)

    async def __call__(self, context: Context, item: Iterable[Iterable[X]]) -> Tuple[Context, List[X]]:
        return context, list(chain(*item))


FLAT_COLLECTOR = FlatCollector()


@dataclass()
class ChainCollector(Collector[Iterable[Iterable[X]], Iterable[X]]):
    logger: Logger = field(default=__logger__, compare=False)

    async def __call__(self, context: Context, item: Iterable[Iterable[X]]) -> Tuple[Context, Iterable[X]]:
        return context, chain(*item)

CHAIN_COLLECTOR = ChainCollector()


@dataclass()
class AnyCollector(Collector[Iterable[X], X]):
    default: X = None
    logger: Logger = field(default=__logger__, compare=False)

    async def __call__(self, context: Context, item: Iterable[X]) -> Tuple[Context, X]:
        try:
            return context, next(iter(item))
        except StopIteration:
            return context, self.default


@dataclass()
class FilterCollector(Collector):
    predicate: Callable[[X], bool]
    logger: Logger = field(default=__logger__, compare=False)

    async def __call__(self, context: Context, item: Iterable) -> Tuple[Context, Iterable]:
        return context, [
            value
            for value in item
            if self.predicate(value)
        ]
