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
"""Implementation of a CLI (Command Line Interface) to command BLITSkrieg.

- Exits with code 0 if everything is OK
- Exits with code 1 when a general client-side error occurs
- Exits with code 64 + <gRPC status code> when a gRPC error is raised by server
(https://github.com/grpc/grpc/blob/master/doc/statuscodes.md)

WARNING: new imports might require updating the package build system
"""

import sys
from configparser import Error as ConfigError
from functools import wraps
from json import dumps
from os import getcwd

from click import argument, echo, group, option, pass_context, version_option
from google.protobuf.json_format import MessageToJson
from grpc import RpcError

from . import __version__
from . import blitskrieg_pb2 as pb
from . import blitskrieg_pb2_grpc as pb_grpc
from . import settings as sett


def _die(message=None, exit_code=1):
    """Print message to stderr with specified error code."""
    if not message:
        message = 'Aborted'
    echo(message, err=True)
    sys.exit(exit_code)


def _check_rpcserver_addr():
    """Check the RPC server address, adding port if missing."""
    if not sett.CLI_RPCSERVER:
        _die('Invalid RPC server address')
    rpcserver = sett.CLI_RPCSERVER.split(':', 1)
    if len(rpcserver) > 1:
        port = rpcserver[1]
        if not port.isdigit():
            _die('Invalid RPC server port')
        if int(port) not in range(1, 65536):
            _die('Invalid RPC server port')
    else:
        sett.CLI_RPCSERVER = sett.CLI_RPCSERVER + ':' + sett.PORT


def _get_cli_options():
    """Set CLI options."""
    # pylint: disable=import-outside-toplevel
    from .utils.common import get_config_parser, set_defaults

    # pylint: enable=import-outside-toplevel
    config = get_config_parser(interactive=True)
    c_values = ['RPCSERVER']
    set_defaults(config, c_values)
    sec = 'bli'
    if not sett.CLI_RPCSERVER:
        sett.CLI_RPCSERVER = config.get(sec, 'RPCSERVER')
        _check_rpcserver_addr()


def _handle_call(func):
    """Decorator to handle a gRPC call to BLITSkrieg."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        """Get start options and run wrapped function."""
        try:
            _get_cli_options()
            stub_name, api, req = func(*args, **kwargs)
            # pylint: disable=import-outside-toplevel
            from .utils.common import connect

            # pylint: enable=import-outside-toplevel
            with connect(stub_name, sett.CLI_RPCSERVER,
                         grpc_proto=pb_grpc) as stub:
                res = getattr(stub, api)(req)
            _print_res(res)
        except RpcError as err:
            # pylint: disable=no-member
            json_err = {'code': err.code().name, 'details': err.details()}
            error = dumps(json_err, indent=4, sort_keys=True)
            _die(error, sett.CLI_BASE_GRPC_CODE + err.code().value[0])
            # pylint: enable=no-member
        except ConfigError as err:
            _die(f'Configuration error: {err}')
        except Exception as err:  # pylint: disable=broad-except
            _die(f'Error, terminating cli: {err}')

    return wrapper


def _print_res(response):
    """Print response using JSON format."""
    echo(
        MessageToJson(response,
                      including_default_value_fields=True,
                      preserving_proto_field_name=True,
                      sort_keys=True))


@group()
@option('--config',
        nargs=1,
        help='Path to bli configuration file '
        '(default ~/.blitskrieg/config)')
@option('--rpcserver',
        nargs=1,
        help='Set host[:port] of BLITSkrieg gRPC server')
@version_option(version=__version__, message='%(version)s')
@pass_context
def entrypoint(_ctx, config, rpcserver):
    """Bli, a CLI for BLITSkrieg.

    Paths are relative to the working directory.
    """
    if config is not None:
        if not config:
            _die('Invalid configuration file')
        # pylint: disable=import-outside-toplevel
        from .utils.common import get_path

        # pylint: enable=import-outside-toplevel
        sett.L_CONFIG = get_path(config, base_path=getcwd())
    if rpcserver is not None:
        sett.CLI_RPCSERVER = rpcserver
        _check_rpcserver_addr()


@entrypoint.command()
@option('--clightning', nargs=1, type=int)
@option('--eclair', nargs=1, type=int)
@option('--electrum', nargs=1, type=int)
@option('--lnd', nargs=1, type=int)
@_handle_call
def createstack(clightning, eclair, electrum, lnd):  # pylint: disable=unused-argument
    """Create a docker stack with the requested LN nodes."""
    req = pb.CreateStackRequest(**locals())
    return 'BlitskriegStub', 'CreateStack', req


@entrypoint.command()
@_handle_call
def getinfo():
    """Get BLITSkrieg info."""
    req = pb.GetInfoRequest()
    return 'BlitskriegStub', 'GetInfo', req


@entrypoint.command()
@_handle_call
def removestack():
    """Remove any existing docker stack."""
    req = pb.RemoveStackRequest()
    return 'BlitskriegStub', 'RemoveStack', req


@entrypoint.command()
@argument('blocks', nargs=1, default=0, type=int)
@option('--address', nargs=1, help='Bitcoin mining address')
@_handle_call
def mine(blocks, address):
    """Mine the requested number of blocks, optionally sending the mining
    reward to a specific address.
    """
    request = pb.MineBlockRequest(blocks=blocks, address=address)
    return 'BitcoinStub', 'MineBlock', request


@entrypoint.command()
@argument('blocks', nargs=1, type=int)
@argument('transactions', nargs=1, type=int)
@option('--n_inputs',
        nargs=1,
        type=int,
        help='number of inputs of each transaction (default 1, max 3)')
@option('--n_outputs',
        nargs=1,
        type=int,
        help='number of outputs of each transaction (default 1, max 3)')
@_handle_call
def gentransactions(blocks, transactions, n_inputs, n_outputs):
    """Generate the requested number of blocks, each containing the requested
    number of transactions with the specified number of inputs and outputs.
    """
    request = pb.GenTransactionsRequest(blocks=blocks,
                                        transactions=transactions,
                                        n_inputs=n_inputs,
                                        n_outputs=n_outputs)
    return 'BitcoinStub', 'GenTransactions', request


@entrypoint.command()
@_handle_call
def getaddress():
    """Get a bitcoin address."""
    request = pb.GetAddressRequest()
    return 'BitcoinStub', 'GetAddress', request


@entrypoint.command()
@argument('address', nargs=1)
@argument('amount', nargs=1, type=float)
@option('--confirmations', nargs=1, type=int)
@_handle_call
def send(address, amount, confirmations):
    """Send the requested amount of BTC to the requested address."""
    request = pb.SendRequest(address=address,
                             amount=amount,
                             confirmations=confirmations)
    return 'BitcoinStub', 'Send', request


@entrypoint.command()
@_handle_call
def fundnodes():
    """Send BTC to all LN nodes."""
    req = pb.FundNodesRequest()
    return 'LightningStub', 'FundNodes', req
