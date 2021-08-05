import asyncio
import logging
import sys

import aogn
from ogn.parser import parse, ParseError

logging.basicConfig(
    stream=sys.stdout,
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s %(module)s %(message)s',
    datefmt='%b %d %H:%M:%S',
)


def process_beacon(raw_message):
    beacon = {}
    try:
        beacon = parse(raw_message)
        #logging.debug(f'beacon: f{beacon}')
        #logging.debug('Received {aprs_type}: {raw_message}'.format(**beacon))
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
    conn = aogn.Client(aprs_user='NO-CALL', )  # aprs_filter='t/s')

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
