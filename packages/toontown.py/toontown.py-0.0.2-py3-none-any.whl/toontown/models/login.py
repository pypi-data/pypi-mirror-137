from dataclasses import dataclass

from .base import BaseAPIModel


__all__ = ['Login', 'FailedLogin', 'PartialLogin', 'DelayedLogin', 'SuccessfulLogin']


class Login(BaseAPIModel):
    """"Wrapper class for /login response

    Returns
    -------
    SuccessfulLogin
        you can now log into Toontown Rewritten with the provided gameserver and cookie

    DelayedLogin
        you are in the login queue and must poll again with the given queueToken

    FailedLogin
        your account is either not verified or is disabled

    PartialLogin
        your account must be authenticated with ToonGuard
    """
    
    def __new__(cls, *args, **kwargs):
        super().__new__(cls, *args, **kwargs)
        
        success = kwargs.get('success')
        if success == 'true':
            return SuccessfulLogin(kwargs.get('gameserver'), kwargs.get('cookie'))
        elif success == 'delayed':
            return DelayedLogin(kwargs.get('eta'), kwargs.get('position'), kwargs.get('queueToken'))

        banner = kwargs.get('banner')

        if success == 'false':
            return FailedLogin(banner)
        elif success == 'partial':
            return PartialLogin(banner, kwargs.get('responseToken'))


@dataclass
class FailedLogin:
    """Login response if your account was not verified or was disabled
    
    Attributes
    ----------
    banner : str
        the server's response to why the login was failed
    """
    banner: str


@dataclass
class PartialLogin:
    """Login response if your account needs to be authenticated with ToonGuard
    
    Attributes
    ----------
    banner : str
        the server's response to why the login is partial

    response_token : str
        the token to verify that the ToonGuard code was sent by you    
    """
    banner: str
    response_token: str


@dataclass
class DelayedLogin:
    """Login response if you are in a queue to log in
    
    Attributes
    ----------
    eta : int
        the estimated time in seconds of when you can expect to log in
        
    position : int
        your position in the queue
        
    queue_token : str
        the token given in the initial delayed response to update your position in the queue
    """
    eta: int
    position: int
    queue_token: str


@dataclass
class SuccessfulLogin:
    """Login response if you are successfully logged into Toontown Rewritten
    
    Attributes
    ----------
    gameserver : str
        Toontown Rewritten's server host used to connect to the game server
        
    cookie : str
        your unique identifier for your current session, DO NOT SHARE
    """
    gameserver: str
    cookie: str
