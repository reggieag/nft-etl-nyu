from web3 import Web3

from lib.web3_eth import W3Eth, parse_address

ETH_ENDPOINT = "wss://mainnet.infura.io/ws/v3/YOURTOKENGOESHERE"
RARI_CONTRACT = "0x60f80121c31a0d46b5279700f9df786054aa5ee5"
START_BLOCK = 10149090
BLOCK_STEP = 4000
OUT_FILENAME = 'rari_transactions.csv'


def parse_rari_entry(entry):
    # The topics contains the parameters passed into the function. For the RARI token, we're looking at Transfer() function calls.
    # Transfer (index_topic_1 address from, index_topic_2 address to, index_topic_3 uint256 tokenId)
    _from = parse_address(entry.topics[1])
    to = parse_address(entry.topics[2])
    tokenId = int(entry.topics[3].hex()[2:], base=16)
    return (_from, to, tokenId)


if __name__ == "__main__":
    w3 = W3Eth(ETH_ENDPOINT)

    rari_filter = {
        "topics": [Web3.keccak(text="Transfer(address,address,uint256)").hex()],
        "address": Web3.toChecksumAddress(RARI_CONTRACT),
    }

    w3.write_entries_to_csv(
        filename=OUT_FILENAME,
        filter=rari_filter,
        parse_entry_fn=parse_rari_entry,
        start_block=START_BLOCK,
    )