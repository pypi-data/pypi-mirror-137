import asyncio
from pathlib import Path

import toontown
import toontown.models


async def main():
    async with toontown.AsyncToontownClient() as client:
        await client.update(Path('/Users/imac/Library/Application Support/Toontown Rewritten'))


asyncio.run(main())
