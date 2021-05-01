import os

from web3 import Web3

from lib.web3_eth import W3Eth, parse_address

ETH_ENDPOINT = f"wss://mainnet.infura.io/ws/v3/{os.getenv('INFURIA_KEY')}"
PUNKS_CONTRACT = "0xb47e3cd837ddf8e4c57f05d70ab865de6e193bbb"
START_BLOCK = 3914495  # https://etherscan.io/tx/0x0885b9e5184f497595e1ae2652d63dbdb2785de2e498af837d672f5765f28430
BLOCK_STEP = 4000
OUT_FILENAME = 'punks_transactions.csv'


def parse_punks_entry(entry):
    # The topics contains the parameters passed into the function. For the RARI token, we're looking at Transfer() function calls.
    # Transfer (index_topic_1 address from, index_topic_2 address to, index_topic_3 uint256 tokenId)
    _from = parse_address(entry.topics[2])
    to = parse_address(entry.topics[3])
    tokenId = int(entry.topics[1].hex()[2:], base=16)
    price_eth = int(entry.data[2:], base=16)/1000000000000000000
    return (entry.blockNumber, entry.transactionIndex, _from, to, tokenId, price_eth)


if __name__ == "__main__":
    w3 = W3Eth(ETH_ENDPOINT)
    rari_filter = {
        "topics": [Web3.keccak(text="PunkBought(uint256,uint256,address,address)").hex()],
        "address": Web3.toChecksumAddress(PUNKS_CONTRACT),
    }
    w3.write_entries_to_csv(
        filename=OUT_FILENAME,
        filter=rari_filter,
        parse_entry_fn=parse_punks_entry,
        start_block=START_BLOCK,
        headers=['block_number', 'transaction_index', 'from_address', 'to_address',  'punk_id', 'price_eth']
    )