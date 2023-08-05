import functools
from typing import Any, Dict

import yaml


__all__ = ['get']


with open('config.yaml', 'r') as file:
    _config: Dict[str, Any] = yaml.load(file, Loader=yaml.FullLoader)


def get(*keys: str) -> Any:
    """Recursively get from config
    
    EX:
    >>> # config.yaml
    >>> http:
    >>>  base: https://base.com
    >>> ...
    >>> # python3
    >>> config.get('http', 'base')
    https://base.com
    """
    return functools.reduce(lambda c, k: c.get(k, {}), keys, _config)
