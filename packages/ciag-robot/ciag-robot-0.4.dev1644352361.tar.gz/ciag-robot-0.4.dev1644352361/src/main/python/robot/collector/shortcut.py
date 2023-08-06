from typing import Any, Dict

from robot.api import Collector, X
from robot.collector import collections as _collections
from robot.collector import core as _core
from robot.collector import object as _object
# noinspection PyUnresolvedReferences
from robot.collector.collections import AnyCollector as any, \
    FilterCollector as filter
# noinspection PyUnresolvedReferences
from robot.collector.core import AsyncFnCollector as afn
# noinspection PyUnresolvedReferences
from robot.collector.core import AsyncForeachCollector as aforeach
# noinspection PyUnresolvedReferences
from robot.collector.core import ConstCollector as const
# noinspection PyUnresolvedReferences
from robot.collector.core import DefaultCollector as default
# noinspection PyUnresolvedReferences
from robot.collector.core import DelayCollector as delay
# noinspection PyUnresolvedReferences
# noinspection PyUnresolvedReferences
from robot.collector.core import FnCollector as fn
# noinspection PyUnresolvedReferences
from robot.collector.core import ForeachCollector as foreach
# noinspection PyUnresolvedReferences
from robot.collector.core import NONE_COLLECTOR as none
# noinspection PyUnresolvedReferences
from robot.collector.core import PipeCollector as pipe
# noinspection PyUnresolvedReferences
from robot.collector.core import TapCollector as tap
# noinspection PyUnresolvedReferences
from robot.collector.core import TupleCollector as tuple
# noinspection PyUnresolvedReferences
from robot.collector.css import CssCollector as css
# noinspection PyUnresolvedReferences
from robot.collector.error import SuppressCollector as suppress
# noinspection PyUnresolvedReferences
from robot.collector.error import ThrowCollector as throw
# noinspection PyUnresolvedReferences
from robot.collector.http import GetCollector as get, \
    UrlCollector as url, \
    RequestCollector as http_request
# noinspection PyUnresolvedReferences
from robot.collector.io import DownloadCollector as download
# noinspection PyUnresolvedReferences
from robot.collector.json import JsonPathCollector as jsonpath
# noinspection PyUnresolvedReferences
from robot.collector.store import StoreCollector as store, \
    CsvCollector as csv, \
    DictCsvCollector as dict_csv
# noinspection PyUnresolvedReferences
from robot.collector.text import RegexCollector as regex
# noinspection PyUnresolvedReferences
from robot.collector.xml import XPathCollector as xpath, \
    AttrCollector as attr, \
    AsTextCollector as as_text, \
    TextCollector as text

noop = lambda: _core.NOOP_COLLECTOR

context = lambda: _core.CONTEXT

flat = lambda: _collections.FLAT_COLLECTOR

chain = lambda: _collections.CHAIN_COLLECTOR


def dict(*args: Collector[X, Dict[str, Any]], **kwargs: Collector[X, Any]) -> Collector[X, Dict[str, Any]]:
    return _core.DictCollector(
        args,
        kwargs
    )


def obj(*args: Collector[X, Dict[str, Any]], **kwargs: Collector[X, Any]) -> Collector[X, _object.Object]:
    dict_collector = _core.DictCollector(
        args,
        kwargs
    )
    return _object.ObjectCollector(dict_collector)
