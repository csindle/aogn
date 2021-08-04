## Introduction

Asynchronous OGN ([Open Glider Network](http://wiki.glidernet.org/)) Client for asyncio and Python that receives the 
planes', gliders', receivers', etc. APRS messages.

Asynchronicity allows a single listener script to execute concurrently other useful tasks
like inserting records into a database, computing aggregate statistics, making web requests,
etc., since there is no blocking function (e.g. `listen()` or `run_forever()`) and 
no callbacks.


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

from aogn import Client


async def example() -> None:
    conn = Client(aprs_user='NO-CALL')
    while True:
        # Get the APRS packet once available:
        raw_message = await conn.packet()
        print(raw_message)

    await conn.disconnect()


if __name__ == '__main__':
    asyncio.run(example())

```

Please see `example_with_ogn_client.py` for a concurrent example.
