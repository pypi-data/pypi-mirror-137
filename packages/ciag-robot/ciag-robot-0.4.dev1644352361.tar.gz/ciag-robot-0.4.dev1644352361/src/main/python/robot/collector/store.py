import csv
import json
import logging
from dataclasses import dataclass, field
from logging import Logger
from typing import Any, Callable, Sequence, Dict, Tuple

from robot.api import Collector, Context

__logger__ = logging.getLogger(__name__)


@dataclass()
class StoreCollector(Collector[Any, str]):
    filename: Collector[Any, str]
    mode: str = 'w+'
    serializer: Callable[[Any], str] = json.dumps
    logger: Logger = field(default=__logger__, compare=False)

    async def __call__(self, context: Context, item: Any) -> Tuple[Context, str]:
        context, filename = await self.filename(context, item)
        with open(filename, self.mode) as output:
            output.write(self.serializer(item))
        return context, filename


@dataclass()
class CsvCollector(Collector[Sequence[Sequence[Any]], str]):
    filename: Collector[Any, str]
    mode: str = 'w+'
    csv_writer_factory = csv.writer
    logger: Logger = field(default=__logger__, compare=False)

    async def __call__(self, context: Context, item: Sequence[Sequence[Any]]) -> Tuple[Context, str]:
        context, filename = await self.filename(context, item)
        with open(filename, self.mode) as output:
            csv_writer = self.csv_writer_factory(output)
            csv_writer.writerows(item)
        return context, filename


@dataclass()
class DictCsvCollector(Collector[Sequence[Dict[str, Any]], str]):
    filename: Collector[Any, str]
    fields: Sequence[str] = None
    mode: str = 'w+'
    csv_writer_factory = csv.DictWriter
    logger: Logger = field(default=__logger__, compare=False)

    async def __call__(self, context: Context, item: Sequence[Dict[str, Any]]) -> Tuple[Context, str]:
        context, filename = await self.filename(context, item)
        fields = self.fields
        with open(filename, self.mode) as output:
            iterable = iter(item)
            try:
                first_item = next(iterable)
            except StopIteration:
                return context, filename
            if fields is None:
                fields = sorted(first_item.keys())
            csv_writer = self.csv_writer_factory(output, fields)
            csv_writer.writeheader()
            csv_writer.writerow(first_item)
            csv_writer.writerows(iterable)
        return context, filename
