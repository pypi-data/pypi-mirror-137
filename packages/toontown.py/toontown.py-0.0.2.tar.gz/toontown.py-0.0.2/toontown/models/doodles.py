from typing import Dict, Iterator, List, Tuple

from .base import BaseAPIModel


__all__ = ['Doodle', 'Playground', 'District', 'Doodles']


class Doodle:
    """Wrapper class for Doodle data
    
    Attributes
    ----------
    dna : str
        the DNA that makes up the Doodle, used for rendering

    rendition : str
        the URL to a rendering of the Doodle, 256x256 .png format

    traits : List[str]
        the list of the Doodle's traits

    cost : int
        how many jellybeans the Doodle costs at the Pet Shop
    """

    __slots__ = ['dna', 'rendition', 'traits', 'cost']

    def __init__(self, *, dna, traits, cost) -> None:
        self.dna: str = dna
        self.rendition: str = f'https://rendition.toontownrewritten.com/render/{dna}/doodle/256x256.png'
        self.traits: List[str] = traits
        self.cost: int = cost


class Playground:
    """Wrapper class for Playground data
    
    Attributes
    ----------
    name : str
        the name of the playground
        
    doodles : List[Doodle]
        the list of doodles in the playground
    """

    __slots__ = ['name', 'doodles']

    def __init__(self, name, doodles) -> None:
        self.name: str = name
        self.doodles: List[Doodle] = [Doodle(**doodle) for doodle in doodles]


class District:
    """Wrapper class for District data
    
    Attributes
    ----------
    name : str
        the name of the district

    playgrounds : Dict[str, Playground]
        a dictionary mapping Playground name to Playground data
    """

    __slots__ = ['name', 'playgrounds']

    def __init__(self, name, **playgrounds) -> None:
        self.name: str = name
        self.playgrounds: Dict[str, Playground] = {pg: Playground(pg, doodles) for pg, doodles in playgrounds.items()}

    def iteritems(self) -> Iterator[Tuple[str, int]]:
        """Return an iterator of the districts and their population"""
        yield from self.playgrounds.items()

    def keys(self) -> List[str]:
        """Returns a list of the district names"""
        return list(self.playgrounds.keys())

    def values(self) -> List[str]:
        """Returns a list of the district populations"""
        return list(self.playgrounds.values())

    def __getitem__(self, district: str) -> int:
        """Returns the population of the given district"""
        return self.playgrounds.__getitem__(district)


class Doodles(BaseAPIModel):
    """"Wrapper class for /doodles response
    
    Attributes
    ----------
    districts : Dict[str, District]
        a dictionary mapping District name to District data
    """
    
    __slots__ = ['districts']

    def __init__(self, **payload) -> None:
        self.districts: Dict[str, District] = {district: District(district, **playgrounds) for district, playgrounds in payload.items()}

    def iteritems(self) -> Iterator[Tuple[str, int]]:
        """Return an iterator of the districts and their population"""
        yield from self.districts.items()

    def keys(self) -> List[str]:
        """Returns a list of the district names"""
        return list(self.districts.keys())

    def values(self) -> List[str]:
        """Returns a list of the district populations"""
        return list(self.districts.values())

    def __getitem__(self, district: str) -> int:
        """Returns the population of the given district"""
        return self.districts.__getitem__(district)