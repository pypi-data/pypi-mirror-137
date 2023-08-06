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
"""Lightning utils module."""

from logging import getLogger

from boltlight import boltlight_pb2 as lpb

from .. import blitskrieg_pb2 as pb
from .. import settings as sett
from .bitcoin import send_btc_to_addr
from .common import connect

LOGGER = getLogger(__name__)


def fund_nodes(ses, _request):
    """Send BTC to all LN nodes."""
    amount = 1
    for node in sett.CURRENT_BOLTLIGHT_NODES:
        with connect('LightningStub', f'{node}:{sett.BOLTLIGHT_PORT}',
                     ses) as stub:
            # pylint: disable=no-member
            req = lpb.NewAddressRequest(addr_type=lpb.Address.NATIVE_SEGWIT)
            # pylint: enable=no-member
            send_btc_to_addr(ses,
                             stub.NewAddress(req).address,
                             amount,
                             confirmations=1)
    return pb.FundNodesResponse(sent_amount=amount * 10**8)
