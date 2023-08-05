from ..exceptions import FailedResponse


class BaseAPIModel:
    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls)

        if kwargs.get('error', None):
            """Sometimes the server will send an error field when there is no cached response"""
            raise FailedResponse(kwargs['error'])
            
        return instance