class FailedResponse(Exception):
    """An exception that is raised whenever the TTR API returns an error response"""
    
    
class SessionNotConnected(Exception):
    """An exception that is raised whenever an API request is attempted before connecting to the client session"""

    def __init__(self) -> None:
        message = 'Client session is not connected'
        super().__init__(message)
