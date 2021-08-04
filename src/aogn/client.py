
import asyncio
import logging
import time
import math

from . import settings


def create_aprs_login(user_name, pass_code, app_name, app_version, aprs_filter=None):
    if not aprs_filter:
        return "user {} pass {} vers {} {}\n".format(user_name, pass_code, app_name, app_version)
    else:
        return "user {} pass {} vers {} {} filter {}\n".format(user_name, pass_code, app_name, app_version, aprs_filter)


def get_sock_peer_ip(writer):
    if sock := writer.get_extra_info('socket'):
        return sock.getpeername()[0]
    return None


class Client:

    def __init__(self, aprs_user: str, aprs_filter: str = '', auto_reconnect: bool = False, ):
        self.aprs_user = aprs_user
        self.aprs_filter = aprs_filter
        self.auto_reconnect = auto_reconnect

        self.__connect_count = 0
        self.__packet_count = 0
        self._writer = None
        self._reader = None
        self._keepalive_last_sent = 0
        self._last_successful_connect = 0

    async def connect(self) -> None:
        self.__connect_count += 1
        try:
            if self.aprs_filter:
                port = settings.APRS_SERVER_PORT_CLIENT_DEFINED_FILTERS
            else:
                port = settings.APRS_SERVER_PORT_FULL_FEED

            self._reader, self._writer = await asyncio.open_connection(settings.APRS_SERVER_HOST, port)

            login = create_aprs_login(self.aprs_user, -1, settings.APRS_APP_NAME,
                                      settings.APRS_APP_VER, self.aprs_filter)
            self._writer.write(login.encode())
            await self._writer.drain()
            self._last_successful_connect = time.perf_counter()

            logging.info(f'Connected to OGN ({settings.APRS_SERVER_HOST}/{get_sock_peer_ip(self._writer)}:{port}) '
                         f'as {self.aprs_user} with filter "{self.aprs_filter}".')

            # for i in range(3):
            #     packet_b = await self._reader.readline()
            #     logging.debug(f'{i}: Reading dummy packet: {packet_b}')

        except Exception as e:
            logging.error('Connect error: {}'.format(e))

    async def __send_keepalive(self) -> bool:
        """
        Send KeepAlive packet if necessary. _writer must be connected.
        :return Whether or not one was sent.
        """
        if (now := time.perf_counter()) - self._keepalive_last_sent > settings.APRS_KEEPALIVE_TIME:
            logging.debug('Sending keepalive to {}'.format(get_sock_peer_ip(self._writer)))
            self._writer.write('#keepalive\n'.encode())
            await self._writer.drain()
            self._keepalive_last_sent = now
            return True
        return False

    async def packet(self) -> str:
        """
        :return: a possibly empty, packet string.
        """
        if not (self._writer and self._reader):
            await self.connect()
            logging.info(f'Connected (count = {self.__connect_count}).')

        await self.__send_keepalive()

        rv = ''
        try:
            # Read packet string from socket
            packet_b = await self._reader.readline()
        except Exception as err:
            logging.error('Could not read packet!!!')
            logging.exception(err)
            return rv

        if not packet_b:
            # Apparently, zero length lines will only be returned after ~30m if keepalives are not being sent...
            logging.warning(f'Empty packet! {packet_b}')
            await self.disconnect()
            sleep_duration = 2
            logging.warning(f'Disconnected. Sleeping for {sleep_duration} seconds.')
            await asyncio.sleep(sleep_duration)
            return rv

        self.__packet_count += 1
        # Dynamically throttle logging:
        mod = min(100_000, 10**math.floor(math.log10(self.__packet_count)))
        if self.__packet_count % mod == 0:
            logging.debug(f'Received {self.__packet_count} packets.')

        ignore_decoding_error = True   ## todo
        try:
            rv = packet_b.strip().decode(errors="replace") if ignore_decoding_error else packet_b.decode()
        except UnicodeDecodeError as err:
            logging.exception(f'UnicodeDecodeError: {err}')
        except Exception as err:
            logging.error('Serious ERROR:')
            logging.exception(err)

        return rv

    async def disconnect(self):
        logging.info('Closing the connection...')
        self._writer.close()
        await self._writer.wait_closed()
        self._writer = None
        self._reader = None
        logging.info('Closed.')

