# aio-ogn

Asynchronous OGN ([Open Glider Network](http://wiki.glidernet.org/)) Client for asyncio and Python that receives the 
planes', gliders', receivers', etc. APRS messages.

Use a library like [python-ogn-client's](https://github.com/glidernet/python-ogn-client) `ogn.parser.parse` to interpret these messages.


## Installation

```
pip install aio-ogn
```

## Usage

Please see `example.py` for a concurrent example.

Simple example:

```python
import asyncio
import logging

from aogn import Client

async def example() -> None:
    conn = Client(aprs_user='NO-CALL', )  # aprs_filter='t/s')

    try:
        while True:
            raw_message = await conn.packet()
            print(raw_message)
    except KeyboardInterrupt:
        logging.info('OGN Gateway stopped.')

    await conn.disconnect()

if __name__ == '__main__':
    asyncio.run(example())
```
