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
"""Generator of a compose file to run LN nodes in docker."""

from logging import getLogger
from os import environ, linesep, path
from subprocess import call, check_output

from .. import settings as sett
from .bitcoin import create_wallet

LOGGER = getLogger(__name__)

HEADER = """
version: "2.4"

services:
"""

NETWORKS = """
networks:
  default:
    external:
      name: blits_default
"""

VOLUMES = """
volumes:
  blockchain:
    driver: local
"""

REGISTRY = environ.get('CI_REGISTRY', 'registry.gitlab.com')
IMAGE_BASE = f"{REGISTRY}/hashbeam/docker"

BITCOIND = """
  bitcoind:
    image: "{IMAGE_BASE}/bitcoind:{version}"
    command: "-fallbackfee=0.0002"
    logging:
      options:
        max-size: "77m"
        max-file: "7"
    cpu_quota: 100000
    cpu_shares: 128
    mem_limit: 1280000000
    memswap_limit: 1280000000
    restart: "unless-stopped"
    stop_grace_period: "3m"
    volumes:
      - blockchain:/srv/app/.bitcoin
"""

BOLTLIGHT = """
  {0}:
    image: "{IMAGE_BASE}/boltlight:{version}"
    logging:
      options:
        max-size: "77m"
        max-file: "7"
    cpu_quota: 100000
    cpu_shares: 128
    mem_limit: 1280000000
    memswap_limit: 1280000000
    restart: "unless-stopped"
    stop_grace_period: "3m"
    volumes:
      - {0}:/srv/app/.boltlight
      - {1}/srv/node/
"""

BOLTLIGHT_VOL = """
  {}:
    driver: local
"""

CLIGHTNING = """
  clightning_{0}:
    image: "{IMAGE_BASE}/c-lightning:{version}"
    logging:
      options:
        max-size: "77m"
        max-file: "7"
    cpu_quota: 100000
    cpu_shares: 128
    mem_limit: 1280000000
    memswap_limit: 1280000000
    restart: "unless-stopped"
    stop_grace_period: "3m"
    command: "--allow-deprecated-apis=false"
    volumes:
      - clightning_data_{0}:/srv/app/.lightning
"""

CLIGHTNING_VOL = """
  clightning_data_{}:
    driver: local
"""

ECLAIR = """
  eclair_{0}:
    image: "{IMAGE_BASE}/eclair:{version}"
    logging:
      options:
        max-size: "77m"
        max-file: "7"
    cpu_quota: 100000
    cpu_shares: 128
    mem_limit: 1280000000
    memswap_limit: 1280000000
    restart: "unless-stopped"
    stop_grace_period: "3m"
    environment:
      BITCOIND_WLT: eclair_{0}
    volumes:
      - eclair_data_{0}:/srv/app/data
"""

ECLAIR_VOL = """
  eclair_data_{}:
    driver: local
"""

ELECTRUM = """
  electrum_{0}:
    image: "{IMAGE_BASE}/electrum:{version}"
    logging:
      options:
        max-size: "77m"
        max-file: "7"
    cpu_quota: 100000
    cpu_shares: 128
    mem_limit: 1280000000
    memswap_limit: 1280000000
    restart: "unless-stopped"
    stop_grace_period: "3m"
    environment:
      WALLET_NAME: wlt
      SRV_HOST: electrs
    volumes:
      - electrum_data_{0}:/srv/wallet
      - {init_sh_abspath}:/srv/app/{init_sh}
"""

ELECTRUM_VOL = """
  electrum_data_{}:
    driver: local
"""

ELECTRS = """
  electrs:
    image: "{IMAGE_BASE}/electrs:{version}"
    logging:
      options:
        max-size: "77m"
        max-file: "7"
    cpu_quota: 100000
    cpu_shares: 128
    mem_limit: 1280000000
    memswap_limit: 1280000000
    restart: "unless-stopped"
    stop_grace_period: "3m"
    volumes:
      - electrs_data:/srv/app/db
"""

ELECTRS_VOL = """
  electrs_data:
    driver: local
"""

LND = """
  lnd_{0}:
    image: "{IMAGE_BASE}/lnd:{version}"
    command: "--noseedbackup"
    logging:
      options:
        max-size: "77m"
        max-file: "7"
    cpu_quota: 100000
    cpu_shares: 128
    mem_limit: 1280000000
    memswap_limit: 1280000000
    restart: "unless-stopped"
    stop_grace_period: "3m"
    hostname: "lnd_{0}"
    environment:
      NO_MACAROONS: 1
      API_ADDR: "lnd_{0}:10009"
    volumes:
      - lnd_data_{0}:/srv/app/.lnd
"""

LND_VOL = """
  lnd_data_{}:
    driver: local
"""

BOLTLIGHT_CFG = """
[boltlight]
implementation = {0}
insecure_connection = 1
[blink]
insecure = 1
[{0}]
"""

BOLTLIGHT_CLIGHTNING_CFG = """
cl_rpc_dir = /srv/node/regtest/
"""

BOLTLIGHT_ECLAIR_CFG = """
ecl_host = eclair_{}
"""

BOLTLIGHT_ELECTRUM_CFG = """
ele_host = electrum_{}
"""

BOLTLIGHT_LND_CFG = """
lnd_host = lnd_{}
lnd_cert_dir = /srv/node/
"""


def create_boltlight_configs(nodes):
    """Create configuration files for all boltlight definitions on compose."""
    for implementation, num_instances in nodes.items():
        for node in range(1, num_instances + 1):
            _prepare_boltlight(implementation.lower(), node)


def create_compose_file(nodes):
    """Create a docker compose file.

    The file must contain the requested nodes and the services they need in
    order to operate.
    """
    compose = _render_compose(nodes)
    list_to_file(compose, sett.COMPOSE_FILE)


def init_nodes(nodes):
    """Execute the LN node initialization script (if it exists)."""
    LOGGER.debug('Initializing nodes')
    for implementation, n_nodes in nodes.items():
        impl = implementation.lower()
        init_sh_path = sett.INIT_SH_RELPATH.format(impl)
        if not path.exists(init_sh_path):
            return
        for node in range(1, n_nodes + 1):
            compose_cmd = (sett.COMPOSE_BASE_CMD +
                           f'exec -T -u {sett.USER} {impl}_{node} '
                           f'/srv/app/{sett.INIT_SH.format(impl)}'.split())
            call(compose_cmd)


def init_nodes_env(ses, nodes):
    """Execute tasks required before running the LN nodes.

    Currently only eclair needs initialization of environment: creating a
    dedicated bitcoind wallet. Without this a 'bitcoind wallet not available'
    error will be logged by eclair.
    """
    for implementation, n_nodes in nodes.items():
        if implementation.lower() != 'eclair':
            continue
        for node in range(1, n_nodes + 1):
            # wallet name must match name in BITCOIND_WLT env var
            create_wallet(ses, f'eclair_{node}')


def lines_to_list(lines):
    """Parse a multi-line string into a list."""
    return lines.split('\n')[1:-1]


def list_to_file(lines, file_path):
    """Write list elements to a file in the specified path.

    Separate elements with new lines.
    """
    with open(file_path, 'w', encoding='utf-8') as file:
        for line in lines:
            file.write(line + linesep)


def _add_node(compose, volumes, n_nodes, implementation):
    """Add LN node and an associated boltlight to compose and volumes lists."""
    init_sh_abspath = sett.INIT_SH_ABSPATH.format(implementation.lower())
    for node in range(1, n_nodes + 1):
        service_version = getattr(sett, f'{implementation}_VER')
        service = globals()[implementation].format(
            node,
            version=service_version,
            IMAGE_BASE=IMAGE_BASE,
            init_sh_abspath=init_sh_abspath,
            init_sh=sett.INIT_SH.format(implementation.lower()))
        vol = lines_to_list(globals()[f'{implementation}_VOL'].format(node))
        node_vol = vol[0].strip()
        boltlight_name = f'boltlight_{implementation.lower()}_{node}'
        boltlight = BOLTLIGHT.format(boltlight_name,
                                     node_vol,
                                     version=sett.BOLTLIGHT_VER,
                                     IMAGE_BASE=IMAGE_BASE)
        compose.extend(lines_to_list(service) + lines_to_list(boltlight))
        boltlight_vol = BOLTLIGHT_VOL.format(boltlight_name)
        volumes.extend(vol + lines_to_list(boltlight_vol))
        sett.CURRENT_BOLTLIGHT_NODES.append(boltlight_name)


def _prepare_boltlight(implementation, node):
    """Prepare a boltlight instance by creating its config file and its DB."""
    config = lines_to_list(BOLTLIGHT_CFG.format(implementation))
    node_cfg = globals()[f'BOLTLIGHT_{implementation.upper()}_CFG'].format(
        node)
    config += lines_to_list(node_cfg)
    list_to_file(config, sett.BOLTLIGHT_DATA + '/config')
    cp_cmd = (f'docker cp {sett.BOLTLIGHT_DATA}/config '
              f'{sett.COMPOSE_PRJ_NAME}_boltlight_{implementation}_{node}_1'
              ':/srv/app/.boltlight/')
    check_output(cp_cmd.split())
    data_abspath = path.join(sett.HOST_WORKDIR, sett.BOLTLIGHT_DATA)
    run_cmd = (f'docker run --rm -v {data_abspath}:/srv/app/.boltlight '
               f'{IMAGE_BASE}/boltlight:{sett.BOLTLIGHT_VER} bash -c')
    run_cmd = run_cmd.split() + [
        f'boltlight_password={sett.PASSWORD} eclair_password={sett.PASSWORD} '
        f'electrum_password={sett.PASSWORD} lnd_password={sett.PASSWORD} '
        'unsafe_secrets=1 /srv/app/.local/bin/boltlight-secure'
    ]
    check_output(run_cmd)
    cp_cmd = (f'docker cp {sett.BOLTLIGHT_DATA}/db/boltlight.db '
              f'{sett.COMPOSE_PRJ_NAME}_boltlight_{implementation}_{node}_1'
              ':/srv/app/.boltlight/db/boltlight.db')
    check_output(cp_cmd.split())


def _render_compose(nodes):
    """Create a docker-compose yaml using lists."""
    compose = lines_to_list(HEADER)
    compose.extend(
        lines_to_list(
            BITCOIND.format(version=sett.BITCOIND_VER, IMAGE_BASE=IMAGE_BASE)))
    networks = lines_to_list(NETWORKS)
    volumes = lines_to_list(VOLUMES)
    if 'ELECTRUM' in nodes and nodes['ELECTRUM'] > 0:
        compose.extend(
            lines_to_list(
                ELECTRS.format(version=sett.ELECTRS_VER,
                               IMAGE_BASE=IMAGE_BASE)))
        volumes.extend(lines_to_list(ELECTRS_VOL))
    for node in nodes.items():
        _add_node(compose, volumes, node[1], node[0])
    compose.extend([""] + networks)
    compose.extend([""] + volumes)
    return compose
