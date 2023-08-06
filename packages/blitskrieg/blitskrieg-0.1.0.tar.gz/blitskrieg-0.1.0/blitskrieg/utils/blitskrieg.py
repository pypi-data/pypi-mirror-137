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
"""Blitskrieg utils module."""

from datetime import datetime
from glob import glob
from logging import getLogger
from os import path, remove
from shutil import rmtree
from subprocess import CalledProcessError, check_output
from time import sleep

from boltlight import boltlight_pb2 as lpb
from grpc import RpcError, StatusCode

from .. import __version__
from .. import blitskrieg_pb2 as pb
from .. import settings as sett
from .bitcoin import gen_blocks
from .common import connect
from .configure_stack import (
    create_boltlight_configs, create_compose_file, init_nodes, init_nodes_env)

LOGGER = getLogger(__name__)


def create_stack(ses, request):
    """Create a docker stack with the requested LN nodes."""
    try:
        _get_stack_down(ses)
        nodes = {
            field.name.upper(): value
            for field, value in request.ListFields()
        }
        create_compose_file(nodes)
        check_output(sett.COMPOSE_BASE_CMD + 'up --no-start'.split())
        check_output(sett.COMPOSE_BASE_CMD + 'up -d bitcoind'.split())
        # mine a block before turning on eclair to avoid
        # 'bitcoind should be synchronized' error
        gen_blocks(ses, load=True)
        if 'ELECTRUM' in nodes and nodes['ELECTRUM'] > 0:
            check_output(sett.COMPOSE_BASE_CMD + 'up -d electrs'.split())
            start = datetime.now()
            ready = False
            while (datetime.now() - start).seconds <= 10:
                try:
                    check_output('curl -fSs electrs:24224'.split())
                    ready = True
                    break
                except CalledProcessError:
                    sleep(1)
            if not ready:
                _create_stack_error(ses.context, 'electrs is unavailable')
        create_boltlight_configs(nodes)
        init_nodes_env(ses, nodes)
        check_output(sett.COMPOSE_BASE_CMD + 'up -d'.split())
        init_nodes(nodes)
        _unlock_boltlight_nodes(ses)
        for node in sett.CURRENT_BOLTLIGHT_NODES:
            _test_node_connection(ses, node)
    except CalledProcessError as err:
        _create_stack_error(ses.context, err)
    except RuntimeError as err:
        _create_stack_error(ses.context, err)
    return pb.CreateStackResponse()


def get_info():
    """Get BLITSkrieg info."""
    return pb.GetInfoResponse(version=__version__)


def remove_stack(ses, _request):
    """Remove any existing docker stack."""
    response = pb.RemoveStackResponse()
    _get_stack_down(ses)
    return response


def _create_stack_error(context, error=None):
    """Terminate RPC call with a create stack error."""
    err_msg = 'Error creating stack'
    if error:
        err_msg += f': {error}'
    context.abort(StatusCode.CANCELLED, err_msg)


def _get_stack_down(ses):
    """If a compose file exists, try to get docker stack down."""
    try:
        if path.exists(sett.COMPOSE_FILE):
            check_output(sett.COMPOSE_BASE_CMD +
                         ' down -v --remove-orphans'.split())
            sett.CURRENT_BOLTLIGHT_NODES = []
            for data in glob(path.join(sett.BOLTLIGHT_DATA, "*")):
                try:
                    rmtree(data)
                except NotADirectoryError:
                    remove(data)
    except CalledProcessError:
        ses.context.abort(StatusCode.CANCELLED, 'Error removing stack')


def _test_node_connection(ses, node):
    """Test node connection.

    Call the GetInfo API, to check whether the node is ready to answer to
    successive calls.
    """
    with connect('LightningStub', f'{node}:{sett.BOLTLIGHT_PORT}',
                 ses) as stub:
        req = lpb.GetNodeInfoRequest()
        attempts = 10
        while attempts:
            try:
                stub.GetNodeInfo(req)
                return
            except RpcError:
                attempts -= 1
                LOGGER.debug('Error testing boltlight connection')
                sleep(3)
        raise RuntimeError('Error testing boltlight connection')


def _unlock_boltlight_nodes(ses):
    """Call the Unlock API on each boltlight's instance."""
    LOGGER.debug('Unlocking boltlight nodes')
    for node in sett.CURRENT_BOLTLIGHT_NODES:
        with connect('UnlockerStub', f'{node}:{sett.BOLTLIGHT_PORT}',
                     ses) as stub:
            req = lpb.UnlockRequest(password=sett.PASSWORD)
            try:
                stub.Unlock(req)
            except RpcError as err:
                # pylint: disable=no-member
                err = err.details() if hasattr(err, 'details') else err
                err_msg = 'Error unlocking boltlight: ' + str(err)
                raise RuntimeError(err_msg) from None
        _unlock_node(ses, node)


def _unlock_node(ses, node):
    """Call the UnlockNode API on each boltlight's instance."""
    with connect('LightningStub', f'{node}:{sett.BOLTLIGHT_PORT}',
                 ses) as stub:
        req = lpb.UnlockNodeRequest(password=sett.PASSWORD)
        attempts = 10
        while attempts:
            try:
                stub.UnlockNode(req)
                LOGGER.debug('Node unlocked')
                return
            except RpcError as err:
                # pylint: disable=no-member
                if err.code() == StatusCode.UNIMPLEMENTED and \
                        'not supported for this implementation' in \
                        err.details():
                    return
                attempts -= 1
                # pylint: disable=no-member
                err = err.details() if hasattr(err, 'details') else err
                err_msg = 'Error unlocking node: ' + str(err)
                LOGGER.debug(err_msg)
                sleep(5)
        raise RuntimeError('Error unlocking node')
