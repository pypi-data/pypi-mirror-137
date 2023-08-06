# BLITSkrieg - a Bitcoin Lightning Integration Test Service
#
# Copyright (C) 2022 hashbeam contributors
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# For a full list of contributors, please see the AUTHORS.md file.
"""The Python implementation of the gRPC BLITSkrieg server."""

import sys
from concurrent import futures
from logging import getLogger
from threading import active_count
from time import sleep, strftime

from grpc import server

from . import __version__
from . import blitskrieg_pb2_grpc as pb_grpc
from . import settings as sett
from .bitcoin import BitcoindRPC, BitcoinServicer
from .lightning import LightningServicer
from .utils.blitskrieg import create_stack, get_info, remove_stack
from .utils.common import (
    BlitsSession, handle_keyboardinterrupt, handle_logs, init_server)
from .utils.exceptions import InterruptException

LOGGER = getLogger(__name__)


class BlitskriegServicer(pb_grpc.BlitskriegServicer):
    """Implement the Blitskrieg service defined with protobuf."""

    @handle_logs
    def CreateStack(self, request, context):
        """CreateStack API implementation."""
        rpc_btc = BitcoindRPC()
        ses = BlitsSession(context, rpc_btc=rpc_btc)
        return create_stack(ses, request)

    @handle_logs
    def GetInfo(self, _request, _context):
        """GetInfo API implementation."""
        return get_info()

    @handle_logs
    def RemoveStack(self, request, context):
        """RemoveStack API implementation."""
        rpc_btc = BitcoindRPC()
        ses = BlitsSession(context, rpc_btc=rpc_btc)
        return remove_stack(ses, request)


def _interrupt_threads():
    """Try to gracefully stop all pending threads of the runtime server."""
    close_event = None
    if sett.RUNTIME_SERVER:
        close_event = sett.RUNTIME_SERVER.stop(sett.GRPC_GRACE_TIME)
    if close_event:
        while not close_event.is_set() or sett.THREADS:
            LOGGER.error('Waiting for %s threads to complete...',
                         active_count())
            sleep(3)
    LOGGER.info('All threads shutdown correctly')


def _log_intro():
    """Print a booting boilerplate to ease run distinction."""
    LOGGER.info(' ' * 72)
    LOGGER.info(' ' * 72)
    LOGGER.info(' ' * 72)
    LOGGER.info('*' * 72)
    LOGGER.info(' ' * 72)
    LOGGER.info('BLITSkrieg')
    LOGGER.info('version %s', __version__)
    LOGGER.info(' ' * 72)
    LOGGER.info('booting up at %s', strftime(sett.LOG_TIMEFMT))
    LOGGER.info(' ' * 72)
    LOGGER.info('*' * 72)


def _log_outro():
    """Print a quitting boilerplate to ease run distinction."""
    LOGGER.info('stopping at %s', strftime(sett.LOG_TIMEFMT))
    LOGGER.info('*' * 37)


@handle_keyboardinterrupt
def _start():
    """Start a gRPC server listening at the specified address."""
    init_server()
    _log_intro()
    LOGGER.debug('Working directory: %s', sett.HOST_WORKDIR)
    grpc_server = server(
        futures.ThreadPoolExecutor(max_workers=sett.GRPC_WORKERS))
    host = f'{sett.HOST}:{sett.PORT}'
    grpc_server.add_insecure_port(host)
    pb_grpc.add_BlitskriegServicer_to_server(BlitskriegServicer(), grpc_server)
    pb_grpc.add_BitcoinServicer_to_server(BitcoinServicer(), grpc_server)
    pb_grpc.add_LightningServicer_to_server(LightningServicer(), grpc_server)
    sett.RUNTIME_SERVER = grpc_server
    grpc_server.start()
    LOGGER.info('Listening on %s (insecure connection)', host)
    while True:
        sleep(sett.ONE_DAY_IN_SECONDS)


def start():
    """BLITSkrieg entrypoint.

    Any raised and uncaught exception will be handled here.
    """
    try:
        _start()
    except InterruptException:
        _interrupt_threads()
        _log_outro()
        sys.exit(0)
