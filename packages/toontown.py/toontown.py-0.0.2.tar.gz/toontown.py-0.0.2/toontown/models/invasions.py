from datetime import datetime
from typing import List

from .base import BaseAPIModel


__all__ = ['Invasion', 'Invasions']


class Invasion:
    """Wrapper class for invasion data
    
    Attributes
    ----------
    district : str
        the district the invasion is in

    as_of : datetime
        when the invasion started

    type : str
        the Cog type of the invasion

    progress : int
        how many cogs were defeated in this invasion

    total : int
        how many cogs that are invading

    is_mega_invasion : bool
        whether or not this is a mega invasion
    """
    def __init__(self, district, **payload) -> None:
        self.district: str = district
        self.as_of = datetime.fromtimestamp(payload.pop('asOf'))
        self.type: str = payload.pop('type')

        progress, total = payload.pop('progress').split('/')
        self.progress = int(progress)
        self.total = int(total)

    @property
    def is_mega_invasion(self) -> bool:
        return self.total == 1000000


class Invasions(BaseAPIModel):
    """"Wrapper class for /invasions response

    Attributes
    ----------
    last_updated : datetime
        the time when the invasions were last updated

    invasions : List[Invasion]
        the list of invasion data for each district
    """

    __slots__ = ['last_updated', 'invasions']
    
    def __init__(self, **payload) -> None:
        self.last_updated = datetime.fromtimestamp(payload.pop('lastUpdated'))
        
        invasions = payload.pop('invasions')
        self.invasions: List[Invasion] = [Invasion(district, **props) for district, props in invasions.items()]