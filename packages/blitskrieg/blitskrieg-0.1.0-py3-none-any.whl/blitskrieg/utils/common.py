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
"""Common utils module."""

from __future__ import print_function

import sys
from argparse import ArgumentParser
from configparser import ConfigParser
from contextlib import contextmanager, suppress
from cProfile import Profile
from distutils.util import strtobool
from functools import wraps
from glob import glob
from logging import getLogger
from logging.config import dictConfig
from os import R_OK, access
from os import environ as env
from os import mkdir, path
from pathlib import Path
from pstats import Stats
from shutil import copyfile
from site import USER_BASE
from time import sleep, time

from boltlight import boltlight_pb2_grpc as lpb_grpc
from grpc import (
    FutureTimeoutError, StatusCode, channel_ready_future, insecure_channel)
from requests import Session as ReqSession
from requests.exceptions import ConnectionError as ReqConnectionErr
from requests.exceptions import Timeout

from .. import settings as sett
from .exceptions import InterruptException

LOGGER = getLogger(__name__)


def die(message=None):
    """Print message to stderr and exits with error code 1."""
    if message:
        sys.stderr.write(message + '\n')
    sys.exit(1)


@contextmanager
def connect(stub_class, server, ses=None, grpc_proto=lpb_grpc, timeout=None):
    """Connect to an insecure gRPC server."""
    channel = None
    channel = insecure_channel(server)
    future_channel = channel_ready_future(channel)
    try:
        future_channel.result(timeout=timeout)
    except FutureTimeoutError:
        # Handle gRPC channel that did not connect
        err_msg = 'Failed to dial server, call timed out'
        if ses:
            ses.context.abort(StatusCode.CANCELLED, err_msg)
        else:
            die(err_msg)
    else:
        stub = getattr(grpc_proto, stub_class)(channel)
        yield stub
        channel.close()


def check_req_params(context, request, *parameters):
    """Raise a missing_parameter error if a param is not in the request."""
    for param in parameters:
        if not getattr(request, param):
            context.abort(StatusCode.INVALID_ARGUMENT,
                          f'Parameter "{param}" is necessary')


def _copy_config_sample(interactive):
    """Copy (or ask to copy) config.sample and exit."""
    if interactive:
        copy = str2bool(input(
            'Missing configuration file, do you want a copy of '
            f'config.sample in the specified location ({sett.CONFIG})? '
            '[Y/n] '),
                        force_true=True)
        if not copy:
            die("You'll need to manually create a configuration file")
    else:
        LOGGER.error('Missing config file, copying sample to "%s"',
                     sett.CONFIG)
    sample = _get_data_files_path('share/doc/' + sett.PKG_NAME,
                                  'examples/config.sample')
    try:
        _try_mkdir(sett.DATA)
        copyfile(sample, sett.CONFIG)
    except OSError as err:
        die('Error copying sample file: ' + str(err))


def _get_data_files_path(install_dir, relative_path):
    """Given a relative path to a data file, return its absolute path.

    If editable pip install / python setup.py develop is detected, use a path
    relative to the source directory (following the .egg-link).
    """
    for base_path in (sys.prefix, USER_BASE, path.join(sys.prefix, 'local')):
        install_path = path.join(base_path, install_dir)
        if path.exists(path.join(install_path, relative_path)):
            return path.join(install_path, relative_path)
        egg_glob = path.join(base_path, 'lib*', 'python*', '*-packages',
                             f'{sett.PIP_NAME}.egg-link')
        egg_link = glob(egg_glob)
        if egg_link:
            with open(egg_link[0], 'r', encoding='utf-8') as f:
                realpath = f.readline().strip()
            if path.exists(path.join(realpath, relative_path)):
                return path.join(realpath, relative_path)
    raise RuntimeError(f'File "{relative_path}" not found')


def get_config_parser(interactive=False):
    """Read config file, setting default values, and return its parser.

    When config is missing, copy config.sample in its expected location and
    terminate.
    """
    if not path.exists(sett.CONFIG):
        _copy_config_sample(interactive)
    config = ConfigParser()
    config.read(sett.CONFIG)
    main_values = ['PORT', 'LOGS_DIR', 'LOGS_LEVEL']
    set_defaults(config, main_values)
    return config


def get_path(ipath, base_path=None):
    """Get absolute posix path.

    By default relative paths are calculated from blitskriegdir.
    """
    ipath = Path(ipath).expanduser()
    if ipath.is_absolute():
        return ipath.as_posix()
    if not base_path:
        base_path = sett.DATA
    return Path(base_path, ipath).as_posix()


def _get_start_options(config):
    """Set BLITSkrieg start options.

    Environmnet variables override configuration file options.
    """
    sec = 'blitskrieg'
    sett.PORT = config.get(sec, 'PORT')
    sett.PORT = env.get('PORT', sett.PORT)
    sett.LOGS_LEVEL = config.get(sec, 'LOGS_LEVEL')
    sett.LOGS_LEVEL = env.get('LOGS_LEVEL', sett.LOGS_LEVEL)
    sett.BOLTLIGHT_ADDR = f'{sett.HOST}:{sett.PORT}'
    sett.BOLTLIGHT_ADDR = env.get('BOLTLIGHT_ADDR', sett.BOLTLIGHT_ADDR)


def handle_keyboardinterrupt(func):
    """Handle KeyboardInterrupt, raising an InterruptException."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except KeyboardInterrupt:
            print('\nKeyboard interrupt detected.')
            raise InterruptException from None

    return wrapper


def _parse_args():
    """Parse command line arguments."""
    parser = ArgumentParser(description='Start BLITSkrieg gRPC server')
    acc_mode = R_OK
    parser.add_argument('--blitskriegdir',
                        metavar='PATH',
                        help="Path containing config file")
    args = vars(parser.parse_args())
    if 'blitskriegdir' in args and args['blitskriegdir'] is not None:
        blitskriegdir = args['blitskriegdir']
        if not blitskriegdir:
            raise RuntimeError('Invalid blitskriegdir: empty path')
        if not path.isdir(blitskriegdir):
            raise RuntimeError(
                'Invalid blitskriegdir: path is not a directory')
        if not access(blitskriegdir, acc_mode):
            raise RuntimeError('Invalid blitskriegdir: permission denied')
        sett.DATA = blitskriegdir
        sett.CONFIG = path.join(sett.DATA, 'config')


def init_server():
    """Initialize server's data directory, logging and config options."""
    _update_logger()
    _parse_args()
    _try_mkdir(sett.DATA)
    _try_mkdir(path.join(sett.DATA, 'logs'))
    config = get_config_parser()
    _get_start_options(config)
    _update_logger(config)


def handle_logs(func):
    """Log gRPC call request and response."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time()
        peer = user_agent = 'unknown'
        request = args[0]
        context = args[1]
        if len(args) == 3:
            request = args[1]
            context = args[2]
        with suppress(ValueError):
            peer = context.peer().split(':', 1)[1]
        for data in context.invocation_metadata():
            if data.key == 'user-agent':
                user_agent = data.value
        LOGGER.info('< %-24s %s %s', request.DESCRIPTOR.name, peer, user_agent)
        response = func(*args, **kwargs)
        response_name = response.DESCRIPTOR.name
        stop_time = time()
        call_time = round(stop_time - start_time, 3)
        LOGGER.info('> %-24s %s %2.3fs', response_name, peer, call_time)
        LOGGER.debug('Full response: %s', str(response).replace('\n', ' '))
        return response

    return wrapper


def profile(func):
    """Activate profiling."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        if not int(env.get('PROFILING', 0)):
            return func(*args, **kwargs)
        LOGGER.info('profiling activated')
        profiler = Profile()
        profiler.enable()
        res = func(*args, **kwargs)
        profiler.disable()
        pstat = Stats(profiler, stream=sys.stdout)
        pstat.print_stats()
        return res

    return wrapper


def set_defaults(config, values):
    """Set configuration defaults."""
    defaults = {}
    for var in values:
        defaults[var] = getattr(sett, var)
    config.read_dict({'DEFAULT': defaults})


def str2bool(string, force_true=False):
    """Cast a string to a boolean, forcing to a default value."""
    try:
        return strtobool(str(string).lower())
    except ValueError:
        return force_true


def _try_mkdir(dir_path):
    """Create a directory if it doesn't exist."""
    if not path.exists(dir_path):
        LOGGER.info('Creating dir %s', dir_path)
        mkdir(dir_path)


def _update_logger(config=None):
    """Activate console logs by default.

    When configuration is available, activate file logs and set configured log
    level.
    """
    if config:
        sec = 'blitskrieg'
        sett.LOGGING['handlers']['console']['level'] = sett.LOGS_LEVEL.upper()
        sett.LOGGING['loggers']['']['handlers'].append('file')
        sett.LOGGING['handlers'].update(sett.LOGGING_FILE)
        sett.LOGS_DIR = get_path(config.get(sec, 'LOGS_DIR'))
        log_path = path.join(sett.LOGS_DIR, sett.LOGS_BLITSKRIEG)
        sett.LOGGING['handlers']['file']['filename'] = log_path
    try:
        dictConfig(sett.LOGGING)
    except (AttributeError, ImportError, TypeError, ValueError) as err:
        err_msg = 'Logging configuration error: ' + str(err)
        raise RuntimeError(err_msg) from None
    getLogger('urllib3').propagate = False


class RPCSession():  # pylint: disable=too-few-public-methods
    """Create and mantain an RPC session open."""

    def __init__(self, auth=None, headers=None, jsonrpc_ver='2.0'):
        self._session = ReqSession()
        self._auth = auth
        self._headers = headers
        self._jsonrpc_ver = jsonrpc_ver
        self._id_count = 0

    # pylint: disable=too-many-arguments
    def call(self, context, data=None, url=None, timeout=None, tries=None):
        """Make an RPC call using the opened session.

        Return the response message and a boolean to signal if it contains an
        error.
        """
        self._id_count += 1
        if url is None:
            url = sett.RPC_URL
        if timeout is None:
            timeout = sett.RPC_READ_TIMEOUT
        if not tries:
            tries = sett.RPC_TRIES
        while True:
            try:
                response = self._session.post(url,
                                              data=data,
                                              auth=self._auth,
                                              headers=self._headers,
                                              timeout=(sett.RPC_CONN_TIMEOUT,
                                                       timeout))
                break
            except ReqConnectionErr:
                tries -= 1
                if tries == 0:
                    context.abort(StatusCode.CANCELLED,
                                  'RPC call failed: max retries reached')
                LOGGER.debug(
                    'Connection failed, sleeping for %.1f secs (%d tries '
                    'left)', sett.RPC_SLEEP, tries)
                sleep(sett.RPC_SLEEP)
            except Timeout:
                context.abort(StatusCode.CANCELLED, 'RPC call timed out')
        if response.status_code not in (200, 500):
            context.abort(
                StatusCode.CANCELLED,
                f'RPC call failed: {response.status_code} {response.reason}')
        json_response = response.json()
        if 'error' in json_response and json_response['error'] is not None:
            err = json_response['error']
            if 'message' in err:
                err = json_response['error']['message']
            LOGGER.debug('RPC err: %s', err)
            return err, True
        if 'result' in json_response:
            LOGGER.debug('RPC res: %s', json_response['result'])
            return json_response['result'], False
        LOGGER.debug('RPC res: %s', json_response)
        return json_response, response.status_code == 500


class BlitsSession():  # pylint: disable=too-few-public-methods
    """Collect session objects necessary at runtime.

    Session objects:
    * gRPC context from client
    * RPC session for bitcoind
    """

    def __init__(self, context=None, rpc_btc=None):
        self.context = context
        if not context:
            self.context = FakeContext()
        self.rpc_btc = rpc_btc


class FakeContext():  # pylint: disable=too-few-public-methods
    """Simulate a gRPC server context in order to (re)define abort().

    This allows checking connection to node before a context is available from
    a client request.
    """

    @staticmethod
    def abort(scode, msg):
        """Raise a runtime error."""
        assert scode
        raise RuntimeError(msg)

    @staticmethod
    def time_remaining():
        """Act as no timeout has been set by client."""
        return None
