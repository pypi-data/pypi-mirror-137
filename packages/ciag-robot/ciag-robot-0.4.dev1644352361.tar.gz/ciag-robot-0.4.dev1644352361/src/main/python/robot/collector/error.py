from __future__ import annotations

import logging
from dataclasses import dataclass, field
from logging import Logger
from typing import Any, Callable, Tuple
from typing import Type

from robot.api import Collector, Context
from robot.api import X, Y
from robot.collector.core import PipeCollector, NONE_COLLECTOR

__logger__ = logging.getLogger(__name__)


@dataclass()
class ThrowCollector(Collector[Any, Any]):
    factory: Callable[[], Exception] = Exception
    logger: Logger = field(default=__logger__, compare=False)

    async def __call__(self, context: Context, item: Any) -> Tuple[Context, Any]:
        raise self.factory()


@dataclass(init=False)
class SuppressCollector(Collector[X, Y]):
    collector: Collector[X, Y]
    handler: Collector[Tuple[Exception, X], Y]
    error_type: Type[Exception] = Exception
    logger: Logger = field(default=__logger__, compare=False)

    def __init__(self, *collector,
                 handler: Collector[Tuple[Exception, X], Y] = NONE_COLLECTOR,
                 error_type: Type[Exception] = Exception,
                 logger: Logger = __logger__):
        self.collector = PipeCollector.from_(collector)
        self.handler = handler
        self.error_type = error_type
        self.logger = logger

    async def __call__(self, context: Context, item: Any) -> Tuple[Context, Any]:
        try:
            return await self.collector(context, item)
        except Exception as ex:
            if isinstance(ex, self.error_type):
                self.logger.debug(f'suppressing exception {ex.__class__.__name__}: {ex}', exc_info=ex)
                return await self.handler(context, (ex, item,))
            else:
                self.logger.info(f'exception was not suppressed {ex.__class__.__name__}: {ex}', exc_info=ex)
                raise ex
