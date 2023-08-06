# Nina-API
A Python API wrapper to retrieve warnings from the german NINA app.

## How to use package

```python
import asyncio

from pynina import Nina, ApiError


async def main():
    try:
        n: Nina = Nina()
        n.addRegion("146270000000")
        await n.update()
    
        for i in n.warnings["146270000000"]:
            print(i)
            print(i.isValid())

    except ApiError as error:
        print(f"Error: {error}")

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()
```