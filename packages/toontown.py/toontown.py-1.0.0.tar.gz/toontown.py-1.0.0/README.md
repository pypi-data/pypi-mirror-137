# toontown.py
A simple Python API wrapper for the Toontown Rewritten API (https://github.com/ToontownRewritten/api-doc/)

## Features
- Asynchronous and synchronous
- API complete

## Installing
**Python 3.8 or higher is required**

```zsh
# Linux/macOS
python3 -m pip install -U toontown.py

# Windows
py -3 -m pip install -U toontown.py
```

## Examples

### Synchronous

```py
>>> import toontown
>>> 
>>> 
>>> toontown = toontown.SyncToontownClient()
>>> toontown.connect()
>>> 
>>> population = toontown.population()
>>> population.total  # Random output
1562
>>> for district, district_population in population.districts():
>>>     print(f'{district} population: {district_population}')
... 
>>> toontown.close()
```

### Asynchronous / Context Manager

```py
>>> import toontown
>>> 
>>> 
>>> async with toontown.AsyncToontownClient() as toontown:
>>>     await toontown.field_offices()
```
