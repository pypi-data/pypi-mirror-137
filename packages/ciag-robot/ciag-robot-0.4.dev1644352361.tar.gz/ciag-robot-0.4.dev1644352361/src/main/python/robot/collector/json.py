from dataclasses import dataclass, field
import logging
from logging import Logger
from typing import Any, Sequence

from jsonpath_ng import parse as parse_jsonpath

from robot.api import Collector, Context
from typing import Tuple
__logger__ = logging.getLogger(__name__)


@dataclass(init=False)
class JsonPathCollector(Collector[Any, Any]):
    logger: Logger = field(default=__logger__, compare=False)

    def __init__(self, jsonpath, logger=__logger__):
        if isinstance(jsonpath, (str,)):
            jsonpath = parse_jsonpath(jsonpath)
        self.jsonpath = jsonpath
        self.logger = logger

    async def __call__(self, context: Context, item: Any) -> Tuple[Context, Sequence[Any]]:
        return context, [
            match.value
            for match in self.jsonpath.find(item)
        ]
