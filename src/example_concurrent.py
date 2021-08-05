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
    conn = aogn.Client(aprs_user='NO-CALL', )  # aprs_filter='t/s')

    try:
        while True:
            # Get the APRS packet once available:
            raw_message = await conn.packet()
            #logging.debug(raw_message)
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
