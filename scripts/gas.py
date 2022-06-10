from brownie import *
from brownie.network import gas_price
from brownie.network.gas.strategies import GasNowStrategy
from scripts.helpers.utils import *

#gas_strategy = GasNowStrategy('fast')
#gas_price(gas_strategy)


whale = accounts[0]
registry = load_registry()

crv_price = coin_price("curve-dao-token")
eth_price = coin_price("ethereum")


def main():
    # Setup -- Deposit to first pool
    first_pool = load_pool_from_index(13)
    seth_rewards = deposit_to_eth_pool(first_pool, whale, 1 * 1e18)
    pools = [ZERO_ADDRESS] * 8
    pools[0] = seth_rewards
    init_eth = accounts[0].balance()

    # Balance if unchanged
    chain.snapshot()
    chain.mine(timedelta=24 * 60 * 60)

    print(f"--- Initial {registry.get_pool_name(first_pool)} ---")
    display_balances(pools, init_eth)

    # Test Redeposit
    chain.revert()
    new_pool = load_pool_from_index(2)
    new_rewards, new_amt = redeposit_eth_pool(whale, first_pool, new_pool)

    pools[0] = new_rewards
    chain.mine(timedelta=24 * 60 * 60)

    print(f"\n--- Redeposit {registry.get_pool_name(new_pool)} ---")
    print(f"Redeposit amount {new_amt / 10 ** 18}")
    display_balances(pools, init_eth)


def display_balances(pools, init_eth):
    crv_amount = calc_cur_value(whale, pools)
    crv_diff = crv_price * crv_amount
    cur_eth = accounts[0].balance()
    eth_diff = eth_price * (cur_eth - init_eth) / 10 ** 18

    print(f"CRV: {crv_amount} @ ${crv_price} = ${crv_diff}")
    print(f"ETH: {(cur_eth - init_eth) / 10 ** 18} @ ${eth_price} = ${eth_diff}")
    print(f"Total: ${crv_diff + eth_diff}")

def calc_gas(num_transactions):
    value = 0
    for i in range(num_transactions):
        index = 0 - i
        tx = history[index]
        print(index, tx.fn_name, tx.gas_price, tx.gas_used)
        value += tx.gas_price * tx.gas_used
        eth_used = value / 10 ** 18
        usd_cost = value / 10 ** 18 * eth_price
        print(f"{eth_used:.{4}f} @ {eth_price} = {usd_cost:.{4}f}")