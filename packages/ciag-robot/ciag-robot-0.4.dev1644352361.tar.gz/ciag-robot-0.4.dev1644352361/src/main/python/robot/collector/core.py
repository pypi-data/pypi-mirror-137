from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass, field
from logging import Logger
from typing import Any, Callable, Iterable, Dict, Tuple, Awaitable, AsyncIterable, Sequence, Union

from robot.api import Collector, Context, X, Y

__logger__ = logging.getLogger(__name__)


@dataclass(init=False)
class PipeCollector(Collector[Any, Any]):
    collectors: Tuple[Collector[Any, Any]]
    logger: Logger = field(default=__logger__, compare=False)

    def __init__(self, *collectors: Collector[Any, Any], logger=__logger__):
        self.collectors = collectors
        self.logger = logger

    async def __call__(self, context: Context, item: Any) -> Tuple[Context, Any]:
        for collector in self.collectors:
            context, item = await collector(context, item)
        return context, item

    @classmethod
    def from_(cls, *collector: Union[Collector, Sequence[Union]]) -> Collector:
        if len(collector) == 0:
            raise Exception()
        if len(collector) > 1:
            return cls(*collector)
        collector = collector[0]
        if isinstance(collector, (tuple, list,)):
            return cls(*collector)
        else:
            return collector


@dataclass(init=False)
class DefaultCollector(Collector[Any, Any]):
    collectors: Tuple[Collector[Any, Any]]
    logger: Logger = field(default=__logger__, compare=False)

    def __init__(self, *collectors: Collector[Any, Any], logger=__logger__):
        self.collectors = collectors
        self.logger = logger

    def is_empty(self, value):
        if value is None:
            return True
        if isinstance(value, (str,)):
            if value.strip() == '':
                return True
            return False
        if isinstance(value, Iterable):
            for item in value:
                if not self.is_empty(item):
                    return False
            return True
        return False

    async def __call__(self, context: Context, item: Any) -> Tuple[Context, Any]:
        for collector in self.collectors:
            context, result = await collector(context, item)
            if not self.is_empty(result):
                return context, result
        return context, None


@dataclass()
class FnCollector(Collector[X, Y]):
    fn: Callable[[X], Y]
    logger: Logger = field(default=__logger__, compare=False)

    async def __call__(self, context: Context, item: X) -> Tuple[Context, Y]:
        return context, self.fn(item)


@dataclass()
class AsyncFnCollector(Collector[X, Y]):
    fn: Callable[[X], Awaitable[Y]]
    logger: Logger = field(default=__logger__, compare=False)

    async def __call__(self, context: Context, item: X) -> Tuple[Context, Y]:
        return context, await self.fn(item)


@dataclass()
class NoopCollector(Collector[X, X]):
    logger: Logger = field(default=__logger__, compare=False)

    async def __call__(self, context: Context, item: X) -> Tuple[Context, X]:
        return context, item


NOOP_COLLECTOR = NoopCollector()


@dataclass()
class ConstCollector(Collector[Any, Y]):
    value: Y
    logger: Logger = field(default=__logger__, compare=False)

    async def __call__(self, context: Context, item: Any) -> Tuple[Context, Y]:
        return context, self.value


NONE_COLLECTOR = ConstCollector(None)


@dataclass(init=False)
class ForeachCollector(Collector[Sequence[X], Sequence[Y]]):
    collector: Collector[X, Y]
    limit: int = None
    logger: Logger = field(default=__logger__, compare=False)

    def __init__(self, *collector: Collector[X, Y], limit: int = None, logger: Logger = __logger__):
        self.collector = PipeCollector.from_(collector)
        self.limit = limit
        self.logger = logger

    async def __call__(self, context: Context, item: Sequence[X]) -> Tuple[Context, Sequence[Y]]:
        all_items = list(i for i in item)
        batch_size = len(all_items) if self.limit is None else self.limit
        batch_size = batch_size or 1
        collected_items = []
        for batch in [all_items[index:index + batch_size] for index in range(0, len(all_items), batch_size)]:
            batch_collected_items = await asyncio.gather(*[
                self.collector(context, i) for i in batch
            ])
            collected_items += batch_collected_items
        return context, list(map(lambda it: it[1], collected_items))


@dataclass(init=False)
class AsyncForeachCollector(Collector[AsyncIterable[X], Sequence[Y]]):
    collector: Union[Collector[X, Y], Sequence[Collector]]
    logger: Logger = field(default=__logger__, compare=False)

    def __init__(self, *collector: Collector[X, Y], logger: Logger = __logger__):
        self.collector = PipeCollector.from_(collector)
        self.logger = logger

    async def __call__(self, context: Context, item: AsyncIterable[X]) -> Tuple[Context, Sequence[Y]]:
        tasks = []
        async for i in item:
            coro = self.collector(context, i)
            task = asyncio.create_task(coro)
            tasks.append(task)
        values = await asyncio.gather(*tasks)
        return context, list(map(lambda it: it[1], values))


@dataclass(init=False)
class TupleCollector(Collector[X, Tuple]):
    collectors: Tuple[Collector[X, Any]]
    logger: Logger = field(default=__logger__, compare=False)

    def __init__(self, *collectors: Collector[X, Any], logger=__logger__):
        self.collectors = collectors
        self.logger = logger

    async def __call__(self, context: Context, item: X) -> Tuple[Context, Tuple]:
        collected_items = await asyncio.gather(*[
            collector(context, item)
            for collector in self.collectors
        ])
        return context, tuple(map(lambda it: it[1], collected_items))


@dataclass()
class DelayCollector(Collector[X, X]):
    delay: float
    logger: Logger = field(default=__logger__, compare=False)

    async def __call__(self, context: Context, item: X) -> Tuple[Context, X]:
        await asyncio.sleep(self.delay)
        return context, item


@dataclass()
class DictCollector(Collector[X, Dict[str, Any]]):
    nested_collectors: Sequence[Collector[X, Dict[str, Any]]] = ()
    field_collectors: Dict[str, Collector[X, Any]] = field(default_factory=dict)
    logger: Logger = field(default=__logger__, compare=False)

    async def __call__(self, context: Context, item: X) -> Tuple[Context, Dict[str, Any]]:
        obj = dict()
        collected_items = await asyncio.gather(*[
            collector(context, item)
            for collector in self.nested_collectors
        ])
        for _, collected_item in collected_items:
            obj.update(collected_item)
        if not self.field_collectors:
            return context, obj
        keys, collectors = zip(*self.field_collectors.items())
        values = await asyncio.gather(*[
            collector(context, item)
            for collector in collectors
        ])
        values = map(lambda it: it[1], values)
        obj.update(dict(zip(keys, values)))
        return context, obj


@dataclass()
class ContextCollector(Collector[Any, Dict[str, Any]]):
    logger: Logger = field(default=__logger__, compare=False)

    async def __call__(self, context: Context, item: Any) -> Tuple[Context, Dict[str, Any]]:
        return context, dict(context)


CONTEXT = ContextCollector()


@dataclass()
class TapCollector(Collector[X, X]):
    collector: Collector[X, Any]
    logger: Logger = field(default=__logger__, compare=False)

    def __post_init__(self):
        self.collector = PipeCollector.from_(self.collector)

    async def __call__(self, context: Context, item: X) -> Tuple[Context, X]:
        await self.collector(context, item)
        return context, item
