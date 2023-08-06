from email import message
import logging
from dataclasses import dataclass, field
from logging import Logger
from typing import Dict, TypeVar, Tuple, Any
from . import HttpParser, HttpParserChain

import aiohttp as _aiothttp

from robot.api import HttpSession, HttpEngine

__logger__: Logger = logging.getLogger(__name__)

T = TypeVar('T')


@dataclass()
class AioHttpSessionAdapter(HttpSession):
    client_session: _aiothttp.ClientSession
    http_parser: HttpParser
    logger: Logger = field(default=__logger__)

    async def download(self, url: str, filename: str):
        self.logger.debug(f'Starting download {url} to {filename}')
        async with self.client_session.get(url, allow_redirects=True) as response:
            if response.status != 200:
                message = f'download {url} failed with status {response.status}'
                self.logger.warning(message)
                raise Exception(message)
            with open(filename, 'wb') as output:
                output.write(await response.read())

    async def request(self, url: str, method = 'GET', body=None) -> Tuple[Dict[str,str], str]:
        self.logger.debug(f'Starting http {method} {url}')
        kwargs = {
            'data' if isinstance(body, (str,bytes),) else 'json' : body
        }
        async with self.client_session.request(method, url, allow_redirects=True, **kwargs) as response:
            if 200 <= response.status <= 299:
                self.logger.info(f'HTTP {method} {url} status {response.status}')
            else:
                message = f'HTTP {method} {url} failed with status {response.status}'
                self.logger.warning(message)
                raise Exception(message)
            content = await response.content.read()
            content_type = response.headers.get('Content-Type', 'text/plain')
            return response.headers, self.parse(content_type, content)

    def parse(self, content_type, content):
        parser = self.http_parser.accept(content_type)
        return parser(content)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        return await self.close()

    async def close(self):
        return await self.client_session.close()

@dataclass

class AioHttpAdapter(HttpEngine):

    aiohttp : Any = field(default=_aiothttp)
    http_parser: HttpParser = field(default_factory=HttpParserChain.default)


    def session(self) -> HttpSession:
        return AioHttpSessionAdapter(self.aiohttp.ClientSession(), self.http_parser)
