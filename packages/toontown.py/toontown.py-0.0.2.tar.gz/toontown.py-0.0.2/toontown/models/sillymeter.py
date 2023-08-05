from datetime import datetime
from typing import Any, Dict, List, Optional

from .base import BaseAPIModel


class SillyTeam:
    """Wrapper class for current rewards in the /sillymeter
    
    Attributes
    ----------
    reward : str
        the reward this Silly Team will give

    description : str
        the description of the reward this Silly Team will give

    points : int
        the amount of points this Silly Team earned in the cycle, 
        set to `None` if the Silly Meter state is not set to `Reward`
    """

    __slots__ = ['reward', 'description', 'points']

    def __init__(self, reward: str, description: str, points: Optional[int]) -> None:
        self.reward = reward
        self.description = description
        self.points = points

    def __str__(self) -> str:
        return self.reward

    def __repr__(self) -> str:
        return self.__str__()


class SillyMeter(BaseAPIModel):
    """Wrapper class for /sillymeter response

    Attributes
    ----------
    state : str
        the current state of the Silly Meter (`Active`, `Reward`, `Inactive`)

    hp : int
        the current HP of the Silly Meter (0 - 5,000,000)

    silly_teams : List[Reward]
        the list of `SillyTeam`s that are in the current Silly Meter

    winner : Optional[str]
        the winning Silly Team whose reward is currently active, otherwise `None`

    next_update_timestamp : datetime
        when the Silly Meter will next update itself

    as_of : datetime
        when the server generated the Silly Meter data
    """

    __slots__ = ['state', 'hp', 'silly_teams', 'winner', 'next_update_timestamp', 'as_of']

    def __init__(self, **payload: Dict[str, Any]) -> None:
        self.state: str = payload.get('state')
        self.hp: int = payload.get('hp')

        rewards: List[str] = payload.get('rewards')
        reward_descriptions: List[str] = payload.get('rewardDescriptions')
        reward_points: List[Optional[int]] = payload.get('rewardPoints')
        self.silly_teams: List[SillyTeam] = list(map(lambda args: SillyTeam(*args), zip(rewards, reward_descriptions, reward_points)))

        self.winner: Optional[str] = payload.get('winner')
        self.next_update_timestamp: datetime = datetime.fromtimestamp(payload.get('nextUpdateTimestamp'))
        self.as_of: datetime = datetime.fromtimestamp(payload.get('asOf'))
