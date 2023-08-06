from __future__ import annotations

import logging
from dataclasses import dataclass

from robot.collector.core import DictCollector, PipeCollector
from robot.collector.object import ObjectCollector, Object
from robot.collector.xml import AsTextCollector
from robot.collector.xml import XPathCollector

__logger__ = logging.getLogger(__name__)


@dataclass()
class OpenGraph(Object):
    title: str = None
    type: str = None
    locale: str = None
    description: str = None
    url: str = None
    site_name: str = None
    image: str = None
    audio: str = None
    video: str = None
    app_id: str = None


dict_opengraph = DictCollector(
    (),
    {
        'title': PipeCollector(
            XPathCollector('//meta[@property="og:title"]/@content'),
            AsTextCollector(),
        ),
        'type': PipeCollector(
            XPathCollector('//meta[@property="og:type"]/@content'),
            AsTextCollector(),
        ),
        'locale': PipeCollector(
            XPathCollector('//meta[@property="og:locale"]/@content'),
            AsTextCollector(),
        ),
        'description': PipeCollector(
            XPathCollector('//meta[@property="og:description"]/@content'),
            AsTextCollector(),
        ),
        'url': PipeCollector(
            XPathCollector('//meta[@property="og:url"]/@content'),
            AsTextCollector(),
        ),
        'site_name': PipeCollector(
            XPathCollector('//meta[@property="og:site_name"]/@content'),
            AsTextCollector(),
        ),
        'image': PipeCollector(
            XPathCollector('//meta[@property="og:image"]/@content'),
            AsTextCollector(),
        ),
        'audio': PipeCollector(
            XPathCollector('//meta[@property="og:audio"]/@content'),
            AsTextCollector(),
        ),
        'video': PipeCollector(
            XPathCollector('//meta[@property="og:video"]/@content'),
            AsTextCollector(),
        ),
        'app_id': PipeCollector(
            XPathCollector('//meta[@property="og:app_id"]/@content'),
            AsTextCollector(),
        ),
    }
)


class OpenGraphCollector(ObjectCollector):

    def __init__(self):
        super().__init__(
            dict_opengraph,
            lambda kwargs: OpenGraph(**kwargs)
        )


OPENGRAPH_COLLECTOR = OpenGraphCollector()

obj_opengraph = lambda: OPENGRAPH_COLLECTOR
