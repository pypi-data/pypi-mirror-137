import asyncio
import bz2
import hashlib
import logging
from multiprocessing.pool import ThreadPool
import os
import sys
import time
from abc import ABC, abstractmethod
from pathlib import Path
from typing import (
    Any,
    Dict,
    Union
)

import aiohttp
import requests
import requests.exceptions

from . import config
from .exceptions import *


logger = logging.getLogger(__name__)


Session = Union[aiohttp.ClientSession, requests.Session]

BASE: str = config.get('http', 'urls', 'base')
BASE_HEADERS: Dict[str, Any] = config.get('http', 'base_headers')
LOGIN_HEADERS: Dict[str, Any] = config.get('http', 'login_headers')

MANIFEST: str = config.get('http', 'urls', 'manifest')
PATCHES: str = config.get('http', 'urls', 'patches')

CHUNK_SIZE: int = config.get('http', 'chunk_size')


class Route:
    def __init__(self, method: str, path: str, **parameters: Any) -> None:
        self.method = method
        self.path = path
        self.parameters = parameters
        self.url = BASE + path

    @property
    def headers(self) -> Dict[str, Any]:
        return LOGIN_HEADERS if self.path == '/login' else BASE_HEADERS


class BaseHTTPClient(ABC):
    @abstractmethod
    def __init__(self) -> None:
        self._session: Session = None

    @abstractmethod
    def connect(self) -> None: ...

    @abstractmethod
    def close(self) -> None: ...

    @abstractmethod
    def request(self, route: Route) -> Any: ...

    @abstractmethod
    def update(self, path: Union[str, Path]) -> None: ...


class SyncHTTPClient(BaseHTTPClient):
    def __init__(self) -> None:
        self._session: requests.Session = None
        self._is_closed = True

    @property
    def is_closed(self) -> bool:
        return self._is_closed

    @is_closed.setter
    def is_closed(self, value: bool) -> None:
        self._is_closed = bool(value)

    def connect(self) -> None:
        self._session = requests.Session()
        self._is_closed = False

    def close(self) -> None:
        self._session.close()
        self._is_closed = True

    def request(self, route: Route) -> Any:
        if self.is_closed:
            raise SessionNotConnected

        method = route.method
        url = route.url
        headers = route.headers
        params = route.parameters

        for tries in range(5):
            try:
                logger.info('Attempting {0} request #{1}: {2}'.format(method, tries+1, url))

                with self._session.request(method, url, params=params, headers=headers) as response:
                    response.raise_for_status()

                    data = response.json()
                    status = response.status_code

                    if 300 > status >= 200:
                        return data

                    if status in {500, 502, 504}:
                        time.sleep(1 + tries * 2)
                        continue

            except requests.exceptions.HTTPError as e:
                message = str(e)
                exc_info = type(e), e, e.__traceback__
                logger.error(message, exc_info=exc_info)

            except OSError as e:
                if tries < 4 and e.errno in {54, 10054}:
                    time.sleep(1 + tries * 2)
                    continue

                logger.info('Exhausted attempts for {0} request: {1}'.format(method, url))
                raise

    def update(self, path: Union[str, Path]) -> None:
        if isinstance(path, str):
            path = Path(path)

        if not path.is_dir():
            raise Exception('Path does not exist or is not a directory')

        manifest = self._session.get(
            MANIFEST,
            headers=BASE_HEADERS,
        ).json()

        files = []

        for file in manifest:
            if sys.platform not in manifest[file]['only']:
                continue

            file_path: Path = path / file
            url = '{0}/{1}'.format(PATCHES, manifest[file]['dl'])

            if not file_path.exists():
                files.append((url, file_path))
                logger.info(f'Queuing {file} for download')
                continue

            hash_alg = hashlib.sha1()
            hash_alg.update(file_path.open('rb').read())

            if manifest[file]['hash'] != hash_alg.hexdigest():
                files.append((url, file_path))
                logger.info(f'Queuing {file} for download')

        def download(args):
            url, file_path = args
            with self._session.get(url, stream=True) as resp:
                logger.info(f'Downloading {url} to {file_path}')
                resp.raise_for_status()
                decompressor = bz2.BZ2Decompressor()

                with open(file_path, 'wb') as file:
                    for chunk in resp.iter_content(chunk_size=CHUNK_SIZE):
                        file.write(decompressor.decompress(chunk))

        with ThreadPool(os.cpu_count()) as pool:
            pool.map(download, files)


class AsyncHTTPClient(BaseHTTPClient):
    def __init__(self) -> None:
        self._session: aiohttp.ClientSession = None

    async def connect(self) -> None:
        self._session = aiohttp.ClientSession(raise_for_status=True)

    async def close(self) -> None:
        await self._session.close()

    async def request(self, route: Route) -> Any:
        if self._session.closed:
            raise SessionNotConnected

        method = route.method
        url = route.url
        headers = route.headers
        params = route.parameters

        for tries in range(5):
            try:
                logger.info('Attempting {0} request #{1}: {2}'.format(method, tries+1, url))

                async with self._session.request(method, url, params=params, headers=headers) as response:
                    data = await response.json()
                    status = response.status

                    if 300 > status >= 200:
                        return data

                    if status in {500, 502, 504}:
                        await asyncio.sleep(1 + tries * 2)
                        continue

            except aiohttp.ClientResponseError as e:
                message = str(e)
                exc_info = type(e), e, e.__traceback__
                logger.error(message, exc_info=exc_info)
                raise

            except OSError as e:
                if tries < 4 and e.errno in {54, 10054}:
                    await asyncio.sleep(1 + tries * 2)
                    continue
                raise

    async def update(self, path: Union[str, Path]) -> None:
        if isinstance(path, str):
            path = Path(path)

        if not path.is_dir():
            raise Exception('Path does not exist or is not a directory')

        manifest = await self._session.get(
            MANIFEST,
            headers=BASE_HEADERS,
        )

        manifest = await manifest.json()

        files = []

        for file in manifest:
            if sys.platform not in manifest[file]['only']:
                continue

            file_path: Path = path / file
            url = '{0}/{1}'.format(PATCHES, manifest[file]['dl'])

            if not file_path.exists():
                files.append((url, file_path))
                logger.info(f'Queuing {file} for download')
                continue

            hash_alg = hashlib.sha1()
            hash_alg.update(file_path.open('rb').read())

            if manifest[file]['hash'] != hash_alg.hexdigest():
                files.append((url, file_path))
                logger.info(f'Queuing {file} for download')

        async def download(args):
            url, file_path = args

            async with self._session.get(url) as resp:
                logger.info(f'Downloading {url} to {file_path}')

                resp.raise_for_status()
                decompressor = bz2.BZ2Decompressor()

                with open(file_path, 'wb') as file:
                    async for chunk in resp.content.iter_chunked(CHUNK_SIZE):
                        file.write(decompressor.decompress(chunk))

        await asyncio.gather(*map(download, files))
