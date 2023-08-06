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
"""Lightning service module."""

from logging import getLogger

from . import blitskrieg_pb2_grpc as pb_grpc
from .bitcoin import BitcoindRPC
from .utils.common import BlitsSession, handle_logs
from .utils.lightning import fund_nodes

LOGGER = getLogger(__name__)


# pylint: disable=too-few-public-methods
class LightningServicer(pb_grpc.LightningServicer):
    """Implement the Lightning service defined with protobuf."""

    @handle_logs
    def FundNodes(self, request, context):
        """FundNodes API implementation."""
        rpc_btc = BitcoindRPC()
        ses = BlitsSession(context, rpc_btc=rpc_btc)
        return fund_nodes(ses, request)


# pylint: enable=too-few-public-methods
