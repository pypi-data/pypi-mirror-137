import logging
import re
from dataclasses import dataclass, field
from logging import Logger
from typing import Union, Sequence, Tuple, Dict

from robot.api import Collector, Context

__logger__ = logging.getLogger(__name__)


@dataclass(init=False)
class RegexCollector(Collector[str, str]):
    logger: Logger = field(default=__logger__, compare=False)

    def __init__(self, regex, logger=__logger__):
        if isinstance(regex, (str,)):
            regex = re.compile(regex)
        self.regex = regex
        self.logger = logger

    async def __call__(self, context: Context, item: str) -> Tuple[Context, Union[str, Sequence[str], Dict]]:
        match = self.regex.search(item)
        if not match:
            return context, None
        group_dict = match.groupdict()
        if group_dict:
            return context, group_dict
        groups = match.groups()
        if len(groups) > 1:
            return context, groups
        elif groups:
            return context, groups[0]
        return context, match.group(0)
