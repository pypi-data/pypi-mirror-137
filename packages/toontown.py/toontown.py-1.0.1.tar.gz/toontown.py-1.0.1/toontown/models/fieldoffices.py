from datetime import datetime
from typing import Iterator, List, Optional

from .base import BaseAPIModel


__all__ = ['FieldOffice', 'FieldOffices']


zone_lookup = {
    '3100': 'Walrus Way',
    '3200': 'Sleet Street',
    '3300': 'Polar Place',
    '4100': 'Alto Avenue',
    '4200': 'Baritone Boulevard',
    '4300': 'Tenor Terrace',
    '5100': 'Elm Street',
    '5200': 'Maple Street',
    '5300': 'Oak Street',
    '9100': 'Lullaby Lane',
    '9200': 'Pajama Place',
}

department_lookup = {
    's': 'Sellbot'
}


class FieldOffice:
    """Wrapper class for field office data
    
    Attributes
    ----------
    last_updated : datetime
        when the field office's data was last updated

    street : str
        the street that the field office is on

    department : str
        the department of the field office (currently only `Sellbot`)

    difficulty : int
        how many stars the field office is

    annexes : int
        how many annexes are left in the field office

    open : bool
        whether or not the elevator to the field office is open

    expiring : Optional[datetime]
        shows how long left the field office will stand after the last annex is defeated, otherwise `None`
    """

    __slots__ = ['last_updated', 'street', 'department', 'difficulty',
                 'annexes', 'open', 'expiring']
    
    def __init__(self, last_updated, zone, *, department, difficulty, annexes, open, expiring) -> None:
        self.last_updated: datetime = last_updated
        self.street: str = zone_lookup[zone]
        self.department: str = department_lookup[department]
        self.difficulty: int = difficulty + 1
        self.annexes: int = annexes
        self.open: bool = open
        self.expiring: Optional[datetime] = datetime.fromtimestamp(expiring) if expiring else None


class FieldOffices(BaseAPIModel):
    """"Wrapper class for /fieldoffices response

    Attributes
    ----------
    last_updated : datetime
        the time when the field offices data was last updated

    field_offices : List[FieldOffice]
        a list of all current field offices, reverse sorted by difficulty (stars)
    """

    __slots__ = ['last_updated', 'field_offices']
    
    def __init__(self, **payload) -> None:
        last_updated = datetime.fromtimestamp(payload.pop('lastUpdated'))
        field_offices = payload.pop('fieldOffices')

        self.last_updated = last_updated
        self.field_offices: List[FieldOffice] = sorted(
            [FieldOffice(last_updated, zone, **props) for zone, props in field_offices.items()],
            key=lambda x: x.difficulty,
            reverse=True,
        )

    def __iter__(self) -> Iterator[FieldOffice]:
        return self.field_offices.__iter__()

    def __next__(self):
        return next(self.field_offices)
