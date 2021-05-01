import os

from web3 import Web3

from lib.web3_eth import W3Eth, parse_address

ETH_ENDPOINT = f"wss://mainnet.infura.io/ws/v3/{os.getenv('INFURIA_KEY')}"
PUNKS_CONTRACT = "0xb47e3cd837ddf8e4c57f05d70ab865de6e193bbb"
# START_BLOCK = 5774644
START_BLOCK = 12346021
END_BLOCK = 12346021
BLOCK_STEP = 4000
OUT_FILENAME = 'punks_transactions.csv'

# https://etherscan.io/tx/0xa7cc3f59c5d3a7a022a1375e607b49059f1b242422dc9986f524012ed744bc2c


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
    # 0x58e5d5a525e3b40bc15abaa38b5882678db1ee68befd2f60bafe3a7fd06db9e3
    rari_filter = {
        "topics": [Web3.keccak(text="PunkBought(uint256,uint256,address,address)").hex()],
        "address": Web3.toChecksumAddress(PUNKS_CONTRACT),
    }
    w3.write_entries_to_csv(
        filename=OUT_FILENAME,
        filter=rari_filter,
        parse_entry_fn=parse_punks_entry,
        start_block=START_BLOCK,
        end_block=END_BLOCK,
    )