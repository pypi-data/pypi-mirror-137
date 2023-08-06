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
"""Bitcoin utils module."""

from decimal import Decimal
from gettext import ngettext
from logging import getLogger
from time import time

from grpc import StatusCode

from .. import blitskrieg_pb2 as pb
from .. import settings as sett
from .common import check_req_params

LOGGER = getLogger(__name__)


def _get_fee_for_utxo(n_inputs, n_outputs):
    """Calculate the fee for a UTXO in the specified transaction."""
    try:
        return Decimal(str(10 + 181 * n_inputs + 34 * n_outputs)) * \
            sett.MIN_RELAY_FEE / Decimal('1000') / Decimal(str(n_outputs))
    except Exception as err:
        raise RuntimeError(err) from None


def _build_vin(inputs):
    """Construct inputs array."""
    vin = []
    for tx_input in inputs:
        vin.append({"txid": tx_input['txid'], "vout": tx_input['vout']})
    return vin


def _build_vout(outputs):
    """Construct outputs array."""
    vout = []
    for tx_output in outputs:
        vout.append({tx_output['address']: float(tx_output['amount'])})
    return vout


def create_wallet(ses, name):
    """Create a bitcoin wallet. May throw a RuntimeError."""
    LOGGER.debug("Creating wallet '%s'", name)
    res, is_err = ses.rpc_btc.createwallet(ses, [str(name)])
    if 'name' not in res and 'Loading wallet...' not in res:
        raise RuntimeError(str(res))
    return name


def _create_raw_tx(ses, wallet, inputs, outputs):
    """Create a raw transaction."""
    req = []
    req.append(_build_vin(inputs))
    req.append(_build_vout(outputs))
    return ses.rpc_btc.createrawtransaction(ses, req, wallet=wallet)[0].strip()


def _get_block_count(ses):
    """Return block height."""
    return ses.rpc_btc.getblockcount(ses)[0]


def _get_miner_utxos(ses):
    """Get enough miner UTXOs in order to reach a total of at least 50 BTC.

    Mine blocks if miner hasn't enough funds.
    """
    height = _get_block_count(ses)
    req_blocks = 101 - height
    if req_blocks > 0:
        gen_blocks(ses)
        height += req_blocks
    era_max_height = sett.HALVING_INTERVAL
    reward = req_amt = sett.MAX_REWARD
    possible_rewards = [reward]
    while True:
        if height < era_max_height:
            break
        reward /= 2
        possible_rewards.append(reward)
        era_max_height += sett.HALVING_INTERVAL
    tot_amt = 0
    utxos = []
    while tot_amt < req_amt:
        if possible_rewards:
            tot_amt = _add_miner_utxos(ses,
                                       utxos,
                                       req_amt,
                                       tot_amt,
                                       reward=possible_rewards.pop(0))
        else:
            gen_blocks(ses)
            height += 1
            tot_amt = _add_miner_utxos(ses, utxos, req_amt, tot_amt)
    return utxos, tot_amt


def _add_miner_utxos(ses, utxos, req_amt, tot_amt, reward=None):
    """Get miner UTXOs until list is exhausted or until tot_amt reaches req_amt.

    If a reward is given, only UTXOs with that amount will be added.
    """
    req = [1, 9999999, [], True]
    if reward:
        req.append({'minimumAmount': reward})
    unspent_utxos, is_err = ses.rpc_btc.listunspent(ses,
                                                    req,
                                                    wallet=sett.MINER_WLT)
    if is_err:
        ses.context.abort(StatusCode.CANCELLED, unspent_utxos)
    for utxo in list(filter(lambda d: d['spendable'] is True, unspent_utxos)):
        tot_amt += utxo['amount']
        utxos.append({
            'txid': utxo['txid'],
            'vout': 0,
            'amount': utxo['amount']
        })
        if req_amt <= tot_amt:
            return tot_amt
    return tot_amt


def _split_coinbase_in_utxos(ses, wallet, num_utxos):
    """Split one or more coinbase TXs in the requested number of UTXOs.

    Split by sending funds to the specified wallet.
    """
    cb_utxos, cb_utxos_amt = _get_miner_utxos(ses)
    LOGGER.debug('Splitting %s coinbase %s in %s %s for a total of %s BTC',
                 len(cb_utxos),
                 ngettext('transaction', 'transactions', len(cb_utxos)),
                 num_utxos, ngettext('UTXO', 'UTXOs', num_utxos), cb_utxos_amt)
    try:
        amt_per_utxo = _divide_btc(cb_utxos_amt, num_utxos)
        fee_per_utxo = _get_fee_for_utxo(len(cb_utxos), num_utxos)
        amt_per_utxo = _subtract_btc(amt_per_utxo, fee_per_utxo)
    except RuntimeError as err:
        ses.context.abort(StatusCode.CANCELLED, str(err))
    addr_list = _get_addresses(ses, wallet, num_utxos)
    outputs = []
    for address in addr_list:
        outputs.append({'address': address, 'amount': amt_per_utxo})
    utxos = _send_raw_tx(ses, sett.MINER_WLT, cb_utxos, outputs)
    gen_blocks(ses)
    return amt_per_utxo, utxos


def get_address(ses, _request):
    """Get a bitcoin address."""
    load_or_create_wlt(ses, sett.MINER_WLT)
    return pb.GetAddressResponse(
        address=_get_addresses(ses, sett.MINER_WLT)[0])


def _get_addresses(ses, wallet, n_addr=1):
    """Generate n_addr bitcoin addresses of the specified wallet."""
    addr_list = []
    attempts = 3
    while len(addr_list) < n_addr and attempts:
        address, is_err = ses.rpc_btc.getnewaddress(ses, wallet=wallet)
        if not is_err:
            addr_list.append(address.strip())
            attempts = 3
        else:
            attempts -= 1
    if len(addr_list) != n_addr:
        ses.context.abort(
            StatusCode.CANCELLED,
            f'Error getting bitcoin addresses from wallet "{wallet}"')
    return addr_list


def gen_transactions(ses, request):
    """Generate the requested number of blocks.

    Each block must contain the requested number of transactions with the
    specified number of inputs and outputs.
    """
    check_req_params(ses.context, request, 'blocks', 'transactions')
    request.n_inputs = 1 if request.n_inputs == 0 else request.n_inputs
    request.n_outputs = 1 if request.n_outputs == 0 else request.n_outputs
    if request.n_inputs > sett.GENTXS_MAX_INPUTS:
        ses.context.abort(
            StatusCode.CANCELLED, 'Requested too many inputs. Max allowed: ' +
            str(sett.GENTXS_MAX_INPUTS))
    if request.n_outputs > sett.GENTXS_MAX_OUTPUTS:
        ses.context.abort(
            StatusCode.CANCELLED, 'Requested too many outputs. Max allowed: ' +
            str(sett.GENTXS_MAX_OUTPUTS))
    if request.n_inputs > request.n_outputs:
        ses.context.abort(
            StatusCode.CANCELLED,
            'The number of inputs cannot be higher than the number of outputs')
    LOGGER.info(
        'Requested %s %s with %s %s (of %s %s and %s %s) each (for a total of '
        '%s %s)', request.blocks, ngettext('block', 'blocks', request.blocks),
        request.transactions,
        ngettext('transaction', 'transactions',
                 request.transactions), request.n_inputs,
        ngettext('input', 'inputs', request.n_inputs), request.n_outputs,
        ngettext('output', 'outputs',
                 request.n_outputs), request.blocks * request.transactions,
        ngettext('transaction', 'transactions', request.transactions))
    load_or_create_wlt(ses, sett.MINER_WLT)
    _gen_transactions(ses, request)
    return pb.GenTransactionsResponse()


def _gen_transactions(ses, request):  # pylint: disable=too-many-locals
    """Generate bitcoin trannsactions.

    Generate the requested number of blocks, creating in each block the
    requested number of transactions (with the specified number of inputs and
    outputs).

    If there more outputs than inputs, those extra outputs will have their
    amount set to the dust value.

    Every time the amount for the next UTXOs will get too low, miner funds
    will be retrieved.
    """
    start_wallet = send_wallet = create_wallet(ses, int(time()))

    input_per_block = request.transactions * request.n_inputs
    output_per_block = request.transactions * request.n_outputs

    available_addresses = sett.MAX_ADDR_PER_WALLET - input_per_block
    remaining_blocks = request.blocks

    amt_per_utxo, next_utxos = _split_coinbase_in_utxos(
        ses, start_wallet, input_per_block)
    fee_per_utxo = _get_fee_for_utxo(request.n_inputs, request.n_outputs)

    extra_outputs = request.n_outputs - request.n_inputs
    not_extra_outputs = request.n_outputs - extra_outputs
    while remaining_blocks:
        recv_wallet = send_wallet
        if available_addresses < request.n_outputs * request.transactions:
            recv_wallet = create_wallet(ses, int(time()))
            available_addresses = sett.MAX_ADDR_PER_WALLET
        try:
            amt_per_utxo = _subtract_btc(amt_per_utxo, fee_per_utxo)
            if extra_outputs:
                amt_per_utxo = _subtract_btc(amt_per_utxo,
                                             (sett.DUST_AMT + fee_per_utxo) *
                                             extra_outputs)
        except RuntimeError as err:
            ses.context.abort(StatusCode.CANCELLED, str(err))
        LOGGER.debug('Amount for next UTXO: %s', amt_per_utxo)
        addr_list = _get_addresses(ses, recv_wallet, output_per_block)
        available_addresses -= output_per_block
        new_utxos = []
        LOGGER.info('Sending %s %s to %s %s (%s %s to go)', input_per_block,
                    ngettext('input', 'inputs',
                             input_per_block), output_per_block,
                    ngettext('output', 'outputs', output_per_block),
                    remaining_blocks,
                    ngettext('block', 'blocks', remaining_blocks))
        LOGGER.debug('Sending from wallet "%s" to wallet "%s"', send_wallet,
                     recv_wallet)
        while addr_list:
            receivers = []
            inputs = []
            for _ in range(not_extra_outputs):
                receivers.append({
                    'address': addr_list.pop(),
                    'amount': amt_per_utxo
                })
            for _ in range(extra_outputs):
                receivers.append({
                    'address': addr_list.pop(),
                    'amount': float(sett.DUST_AMT)
                })
            for _ in range(request.n_inputs):
                inp = next_utxos.pop()
                while int(inp['amount'].compare(sett.DUST_AMT)) <= 0:
                    inp = next_utxos.pop()
                inputs.append(inp)
            new_utxos.extend(_send_raw_tx(ses, send_wallet, inputs, receivers))
        gen_blocks(ses)
        remaining_blocks -= 1
        if amt_per_utxo <= sett.DUST_AMT + fee_per_utxo:
            amt_per_utxo, new_utxos = _split_coinbase_in_utxos(
                ses, send_wallet, input_per_block)
        next_utxos = new_utxos.copy()
        send_wallet = recv_wallet


def load_or_create_wlt(ses, wallet):
    """Load the specified wallet, creating it if it doesn't exist."""
    LOGGER.debug('Loading wallet "%s"', wallet)
    loaded = _load_wallet(ses, wallet)
    if not loaded:
        create_wallet(ses, wallet)


def _load_wallet(ses, wallet):
    """Load a bitcoin wallet."""
    res, is_err = ses.rpc_btc.loadwallet(ses, [wallet])
    if is_err:
        if 'Duplicate -wallet filename specified' in res:
            return True
        if 'already loaded' in res:
            return True
        return False
    return True


def mine_block(ses, request, log=False):
    """Mine the requested number of blocks.

    Optionally send the mining reward to a specific address.
    """
    blocks = request.blocks if request.blocks != 0 else 1
    load_or_create_wlt(ses, sett.MINER_WLT)
    hashes = gen_blocks(ses, num_blocks=blocks, address=request.address)
    if log:
        LOGGER.info('Mined %s %s', blocks, ngettext('block', 'blocks', blocks))
    return pb.MineBlockResponse(block_hashes=hashes,
                                height=_get_block_count(ses))


def gen_blocks(ses, num_blocks=1, address=None, load=False):
    """Generate the requested number of blocks (1 by default).

    Give rewards to the requested address (by default to a miner wallet
    address).

    If load is set to True, miner wallet will be created or loaded.
    """
    if load:
        load_or_create_wlt(ses, sett.MINER_WLT)
    req = [num_blocks]
    if not address:
        address = _get_addresses(ses, sett.MINER_WLT)[0]
    req.append(address)
    return ses.rpc_btc.generatetoaddress(ses, req)[0]


def send(ses, request):
    """Send the requested amount of BTC to the requested address."""
    txid = send_btc_to_addr(ses,
                            request.address,
                            request.amount,
                            confirmations=request.confirmations)
    return pb.SendResponse(txid=txid)


def send_btc_to_addr(ses, address, amount, confirmations=0):
    """Send the requested amount of BTC to the requested address.

    Then mine as many blocks as the requested number of confirmations.
    """
    load_or_create_wlt(ses, sett.MINER_WLT)
    balance, is_err = _get_balance(ses, sett.MINER_WLT)
    if is_err:
        ses.context.abort(StatusCode.CANCELLED, balance)
    miner_addr = _get_addresses(ses, sett.MINER_WLT)[0]
    while balance < amount:
        mine_req = [51, miner_addr]
        ses.rpc_btc.generatetoaddress(ses, mine_req)
        balance, is_err = ses.rpc_btc.getbalance(ses, wallet=sett.MINER_WLT)
    send_req = [address, amount]
    txid, is_err = ses.rpc_btc.sendtoaddress(ses,
                                             send_req,
                                             wallet=sett.MINER_WLT)
    if confirmations:
        mine_req = [confirmations, miner_addr]
        ses.rpc_btc.generatetoaddress(ses, mine_req, wallet=sett.MINER_WLT)
    return txid


def _get_balance(ses, wallet):
    """Get the balance of the specified wallet."""
    return ses.rpc_btc.getbalance(ses, wallet=wallet)


def _send_raw_tx(ses, wallet, inputs, outputs):
    """Send a raw transaction."""
    raw_tx = _create_raw_tx(ses, wallet, inputs, outputs)
    signed_raw_tx = _sign_raw_tx(ses, wallet, raw_tx)
    txid, is_err = ses.rpc_btc.sendrawtransaction(ses, [signed_raw_tx],
                                                  wallet=wallet)
    txid = txid.strip()
    utxos = []
    for i, output in enumerate(outputs):
        amt = Decimal(str(output['amount']))
        utxos.append({'txid': txid, 'vout': i, 'amount': amt})
    return utxos


def _sign_raw_tx(ses, wallet, unsigned_raw_tx):
    """Sign a raw transaction."""
    return ses.rpc_btc.signrawtransactionwithwallet(ses, [unsigned_raw_tx],
                                                    wallet=wallet)[0]['hex']


def _subtract_btc(minuend, subtrahend):
    """Subtract bitcoins using Decimal and quantizing result."""
    try:
        amt = Decimal(str(minuend)) - Decimal(str(subtrahend))
        return amt.quantize(sett.BITCOIN_PRECISION)
    except Exception as err:
        raise RuntimeError('Invalid operation: ' + str(err)) from None


def _divide_btc(dividend, divisor):
    """Divide bitcoins using Decimal and quantizing result."""
    try:
        amt = Decimal(str(dividend)) / Decimal(str(divisor))
        return amt.quantize(sett.BITCOIN_PRECISION)
    except Exception as err:
        raise RuntimeError('Invalid operation: ' + str(err)) from None
