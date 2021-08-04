# aogn

Asynchronous OGN ([Open Glider Network](http://wiki.glidernet.org/)) Client for asyncio and Python that receives the 
planes', gliders', receivers', etc. APRS messages.

Use a library like [python-ogn-client's](https://github.com/glidernet/python-ogn-client) `ogn.parser.parse` to interpret these messages.


## Installation

```
pip install aogn
```

## Usage

Please see `example.py` for a concurrent example.

Simple example:

```python
import asyncio
import logging
import sys

logging.basicConfig(
    stream=sys.stdout,
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s %(module)s %(message)s',
    datefmt='%b %d %H:%M:%S',
)

from aogn import Client


async def example() -> None:
    conn = Client(aprs_user='NO-CALL', )

    try:
        while True:
            # Get the APRS packet once available:
            raw_message = await conn.packet()
            logging.debug(raw_message)
    except KeyboardInterrupt:
        logging.info('OGN Gateway stopped.')

    await conn.disconnect()


if __name__ == '__main__':
    asyncio.run(example())

```
