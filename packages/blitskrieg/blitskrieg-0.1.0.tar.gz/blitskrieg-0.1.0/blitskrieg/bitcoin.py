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
"""Bitcoin stack module."""

from json import dumps
from logging import getLogger

from . import blitskrieg_pb2_grpc as pb_grpc
from . import settings as sett
from .utils.bitcoin import (
    gen_transactions, get_address, load_or_create_wlt, mine_block, send)
from .utils.common import BlitsSession, RPCSession, handle_logs, profile

LOGGER = getLogger(__name__)


class BitcoinServicer(pb_grpc.BitcoinServicer):
    """Implement the Bitcoin service defined with protobuf."""

    @handle_logs
    @profile
    def GenTransactions(self, request, context):
        """GenTransactions API implementation."""
        rpc_btc = BitcoindRPC()
        ses = BlitsSession(context, rpc_btc=rpc_btc)
        return gen_transactions(ses, request)

    @handle_logs
    @profile
    def GetAddress(self, request, context):
        """GetAddress API implementation."""
        rpc_btc = BitcoindRPC()
        ses = BlitsSession(context, rpc_btc=rpc_btc)
        return get_address(ses, request)

    @handle_logs
    @profile
    def MineBlock(self, request, context):
        """MineBlock API implementation."""
        rpc_btc = BitcoindRPC()
        ses = BlitsSession(context, rpc_btc=rpc_btc)
        return mine_block(ses, request, log=True)

    @handle_logs
    @profile
    def Send(self, request, context):
        """Send API implementation."""
        rpc_btc = BitcoindRPC()
        ses = BlitsSession(context, rpc_btc=rpc_btc)
        return send(ses, request)


class BitcoindRPC(RPCSession):
    """Create and mantain an RPC session with bitcoind."""

    def __init__(self):
        self._url = sett.BITCOIND_RPC_URL
        super().__init__(headers={'content-type': 'application/json'})

    def __getattr__(self, name):

        def call_adapter(ses, req=None, timeout=None, tries=None, wallet=None):
            # pylint: disable=super-with-arguments
            url, _, params = self._parse_req(req, wallet=wallet)
            payload = self._construct_payload(name, params)
            if not wallet:
                return super(BitcoindRPC, self).call(ses.context,
                                                     payload,
                                                     url,
                                                     timeout=timeout,
                                                     tries=tries)
            res = None
            is_err = True
            attempts = 3
            # handle wallet reload or creation
            while wallet and is_err and attempts:
                res, is_err = super(BitcoindRPC, self).call(ses.context,
                                                            payload,
                                                            url,
                                                            timeout=timeout,
                                                            tries=tries)
                if is_err and 'wallet does not exist or is not loaded' in res:
                    load_or_create_wlt(ses, wallet)
                attempts -= 1
            # pylint: enable=super-with-arguments

            return res, is_err

        return call_adapter

    def _construct_payload(self, method, params):
        """Construct RPC payload."""
        if not params:
            params = []
        payload = dumps({
            "id": self._id_count,
            "method": method,
            "params": params,
            "jsonrpc": self._jsonrpc_ver
        })
        LOGGER.debug("RPC req: %s", payload)
        return payload

    def _parse_req(self, request, wallet=None):
        """Parse RPC request to get its url, method and parameters."""
        call_url = self._url
        if wallet:
            call_url += '/wallet/' + str(wallet)
        if not request:
            return call_url, None, []
        # return a copy of request in order to avoid changing the original one
        return call_url, None, request[:]
