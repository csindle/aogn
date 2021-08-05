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
