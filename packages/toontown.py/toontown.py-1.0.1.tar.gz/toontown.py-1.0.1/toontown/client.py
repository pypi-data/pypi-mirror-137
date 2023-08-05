"""TODO: Document (A)SyncToontownClient"""

from abc import abstractmethod, ABC
from pathlib import Path
from typing import Optional, Union

from .models import *
from .httpclient import BaseHTTPClient, SyncHTTPClient, AsyncHTTPClient, Route


class BaseToontownClient(ABC):
    @abstractmethod
    def __init__(self, httpclient: BaseHTTPClient) -> None:
        self.http = httpclient

    @abstractmethod
    def connect(self) -> None: ...

    @abstractmethod
    def close(self) -> None: ...

    @abstractmethod
    def doodles(self) -> Doodles: ...

    @abstractmethod
    def field_offices(self) -> FieldOffices: ...

    @abstractmethod
    def invasions(self) -> Invasions: ...

    @abstractmethod
    def login(
        self, 
        *, 
        username: Optional[str] = None, 
        password: Optional[str] = None,
        response_token: Optional[str] = None,
        queue_token: Optional[str] = None,
    ) -> Login: ...

    @abstractmethod
    def population(self) -> Population: ...

    @abstractmethod
    def silly_meter(self) -> None: ...


class SyncToontownClient(BaseToontownClient):
    """Synchronous client to interact with the Toontown Rewritten API"""

    def __init__(self) -> None:
        super().__init__(SyncHTTPClient())

    def connect(self) -> None:
        """Connect to the HTTP client
        
        Must be called before using any other methods in this class
        """
        self.http.connect()

    def close(self) -> None:
        """Closes connection to the HTTP client"""
        self.http.close()

    def doodles(self) -> Doodles:
        """Request Doodle data from the Toontown Rewritten API"""
        data = self.http.request(Route(
            'GET',
            '/doodles'
        ))

        return Doodles(**data)

    def field_offices(self) -> FieldOffices:
        """Request Field Office data from the Toontown Rewritten API"""
        data = self.http.request(Route(
            'GET',
            '/fieldoffices'
        ))

        return FieldOffices(**data)

    def invasions(self) -> Invasions:
        """Request Invasion data from the Toontown Rewritten API"""
        data = self.http.request(Route(
            'GET',
            '/invasions'
        ))

        return Invasions(**data)

    def login(
        self, 
        *, 
        username: Optional[str] = None, 
        password: Optional[str] = None,
        response_token: Optional[str] = None,
        queue_token: Optional[str] = None,
    ) -> Login:
        """Request to log into Toontown Rewritten's game server

        Must provide a username and password, a response token, or a queue token
        
        Parameters
        ----------
        username : Optional[str] = None
            optional username parameter, must also provide password if given

        password : Optional[str] = None
            optional password parameter, must also provide username if given

        response_token : Optional[str] = None
            optional response token parameter, obtained after initial login request with username and password 
            if you are required to authenticate with ToonGuard

        queue_token : Optional[str] = None
            optional queue token parameter, obtained after intial login request with username and password or 
            response token if you are required to wait in the login queue
        """
        params = {'format': 'json'}

        if response_token is not None:
            params['responseToken'] = response_token
        elif queue_token is not None:
            params['queueToken'] = queue_token
        elif username is not None and password is not None:
            params['username'] = username
            params['password'] = password
        else:
            raise Exception('Please provide either a username and password, a queue token, or a response token to log in')

        data = self.http.request(Route(
            'POST',
            '/login',
            **params
        ))
        
        return Login(**data)

    def population(self) -> Population:
        """Request Population data from the Toontown Rewritten API"""
        data = self.http.request(Route(
            'GET',
            '/population'
        ))

        return Population(**data)

    def silly_meter(self) -> None:
        """Request Silly Meter data from the Toontown Rewritten API"""
        data = self.http.request(Route(
            'GET',
            '/sillymeter'
        ))

        return SillyMeter(**data)

    def update(self, path: Union[str, Path]) -> None:
        """Update Toontown Rewritten at the given `path`"""
        self.http.update(path)

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, *args):
        self.close()


class AsyncToontownClient(BaseToontownClient):
    """Asynchronous client to interact with the Toontown Rewritten API"""

    def __init__(self) -> None:
        super().__init__(AsyncHTTPClient())

    async def connect(self) -> None:
        """Connect to the HTTP client
        
        Must be called before using any other methods in this class
        """
        await self.http.connect()

    async def close(self) -> None:
        """Closes connection to the HTTP client"""
        await self.http.close()

    async def doodles(self) -> Doodles:
        """Request Doodle data from the Toontown Rewritten API"""
        data = await self.http.request(Route(
            'GET',
            '/doodles'
        ))

        return Doodles(**data)

    async def field_offices(self) -> FieldOffices:
        """Request Field Office data from the Toontown Rewritten API"""
        data = await self.http.request(Route(
            'GET',
            '/fieldoffices'
        ))

        return FieldOffices(**data)

    async def invasions(self) -> Invasions:
        """Request Invasion data from the Toontown Rewritten API"""
        data = self.http.request(Route(
            'GET',
            '/invasions'
        ))

        return Invasions(**data)

    async def login(
        self, 
        *, 
        username: Optional[str] = None, 
        password: Optional[str] = None,
        response_token: Optional[str] = None,
        queue_token: Optional[str] = None,
    ) -> Login:
        """Request to log into Toontown Rewritten's game server

        Must provide a username and password, a response token, or a queue token
        
        Parameters
        ----------
        username : Optional[str] = None
            optional username parameter, must also provide password if given

        password : Optional[str] = None
            optional password parameter, must also provide username if given

        response_token : Optional[str] = None
            optional response token parameter, obtained after initial login request with username and password 
            if you are required to authenticate with ToonGuard

        queue_token : Optional[str] = None
            optional queue token parameter, obtained after intial login request with username and password or 
            response token if you are required to wait in the login queue
        """
        params = {'format': 'json'}

        if response_token is not None:
            params['responseToken'] = response_token
        elif queue_token is not None:
            params['queueToken'] = queue_token
        elif username is not None and password is not None:
            params['username'] = username
            params['password'] = password
        else:
            raise Exception('Please provide either a username and password, a queue token, or a response token to log in')

        data = await self.http.request(Route(
            'POST',
            '/login',
            **params
        ))
        
        return Login(**data)

    async def population(self) -> Population:
        """Request Population data from the Toontown Rewritten API"""
        data = await self.http.request(Route(
            'GET',
            '/population'
        ))

        return Population(**data)

    async def silly_meter(self) -> None:
        """Request Silly Meter data from the Toontown Rewritten API"""
        data = await self.http.request(Route(
            'GET',
            '/sillymeter'
        ))

        return SillyMeter(**data)

    async def update(self, path: Union[str, Path]) -> None:
        """Update Toontown Rewritten at the given `path`"""
        await self.http.update(path)

    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, *args):
        await self.close()
