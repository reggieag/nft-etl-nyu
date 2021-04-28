from web3 import Web3

from lib.web3_eth import W3Eth, parse_address

ETH_ENDPOINT = "wss://mainnet.infura.io/ws/v3/YOURTOKEN"
OPENSEA_CONTRACT = "0x7be8076f4ea4a4ad08075c2508e481d6c946d12b"
# START_BLOCK = 5774644
START_BLOCK = 12296607
END_BLOCK = 12296607
BLOCK_STEP = 4000
OUT_FILENAME = 'opensea_transactions.csv'

# https://etherscan.io/tx/0xa7cc3f59c5d3a7a022a1375e607b49059f1b242422dc9986f524012ed744bc2c


def parse_opensea_entry(entry):
    # The topics contains the parameters passed into the function. For the RARI token, we're looking at Transfer() function calls.
    # Transfer (index_topic_1 address from, index_topic_2 address to, index_topic_3 uint256 tokenId)
    print(entry)
    _from = parse_address(entry.topics[1])
    to = parse_address(entry.topics[2])
    tokenId = int(entry.topics[3].hex()[2:], base=16)
    return (_from, to, tokenId)


if __name__ == "__main__":
    w3 = W3Eth(ETH_ENDPOINT)

    rari_filter = {
        "topics": [Web3.keccak(text="OrdersMatched(bytes32,bytes32,address,address,uint256,bytes32)").hex()],
        "address": Web3.toChecksumAddress(OPENSEA_CONTRACT),
    }
    Web3.keccak(0xc3d58168c5ae7397731d063d5bbf3d657854427343f4c083240f7aacaa2d0f62)
    w3.write_entries_to_csv(
        filename=OUT_FILENAME,
        filter=rari_filter,
        parse_entry_fn=parse_opensea_entry,
        start_block=START_BLOCK,
        end_block=END_BLOCK,
    )