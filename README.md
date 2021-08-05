## Introduction

**AOGN** is an **A**synchronous **OGN** ([Open Glider Network](http://wiki.glidernet.org/)) client for modern Python.
It connects to the APRS servers and receives the planes', gliders', receivers', etc. APRS messages, 
while still allowing you control of the program flow.

This can simplify programs since:
1. There are no callback or blocking functions (e.g. `listen()` or `run_forever()`).
2. One script/thread/process can still do other useful out-of-band tasks like
computing aggregate statistics and making web requests.

To interpret the raw OGN messages, use a function like
[python-ogn-client's](https://github.com/glidernet/python-ogn-client) `ogn.parser.parse`.


## Installation

```
pip install aogn
```

## Usage

Basic example:

```python
import asyncio
import logging
import sys

import aogn

logging.basicConfig(
    stream=sys.stdout,
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s %(module)s %(message)s',
    datefmt='%b %d %H:%M:%S',
)


async def example() -> None:
    conn = aogn.Client(aprs_user='NO-CALL', )

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

---


Concurrent example, with raw_message [parsing](https://github.com/glidernet/python-ogn-client):

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

from ogn.parser import parse, ParseError


def process_beacon(raw_message):
    beacon = {}
    try:
        beacon = parse(raw_message)
    except ParseError as err:
        logging.warning(f'ParseError: {err}')
    except NotImplementedError as err:
        logging.error(f'NotImplementedError: {err}')
    except AttributeError as err:
        logging.error(f'raw_message: {raw_message}')
        logging.error(f'beacon: {beacon}')
        logging.error(err)
    return beacon


async def example() -> None:
    conn = Client(aprs_user='NO-CALL', )  # aprs_filter='t/s')

    try:
        while True:
            raw_message = await conn.packet()
            if raw_message:
                beacon = process_beacon(raw_message)
    except KeyboardInterrupt:
        logging.info('OGN Gateway stopped.')

    await conn.disconnect()


async def another_io_function() -> None:
    import random

    while True:
        sleep_duration = 120 * random.random()
        logging.debug(f'Concurrently sleeping for {sleep_duration:.0f} seconds...')
        await asyncio.sleep(sleep_duration)


async def main():
    await asyncio.gather(example(), another_io_function())


if __name__ == '__main__':
    asyncio.run(main())
```


