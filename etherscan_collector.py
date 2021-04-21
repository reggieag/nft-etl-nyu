import csv

from web3 import Web3
from urllib.parse import urlparse

ETH_ENDPOINT = "wss://mainnet.infura.io/ws/v3/f9667be3f31d4159b9310bdd152bc0a0"
BLOCK_STEP = 4000

# OPENSEA_CONTRACT = "0x7be8076f4ea4a4ad08075c2508e481d6c946d12b"
RARI_CONTRACT = "0x60f80121c31a0d46b5279700f9df786054aa5ee5"


class W3Eth:
    def __init__(self, endpoint):
        self.endpoint = endpoint
        self._w3 = None

    @property
    def w3(self):
        if self._w3 is not None:
            return self._w3
        url = urlparse(self.endpoint)
        if url.scheme == 'wss':
            self._w3 = Web3(Web3.WebsocketProvider(ETH_ENDPOINT))
        elif url.scheme == 'https' or url.scheme == 'http':
            self._w3 = Web3(Web3.HTTPProvider(ETH_ENDPOINT))
        return self._w3

    def get_entries_batch(self, filter_params, starting_block=None, ending_block=None):
        cur_block = starting_block or 0
        ending_block = ending_block or self.w3.eth.blockNumber
        print(cur_block, ending_block)
        while cur_block <= ending_block:
            filter_params.update(
                {"fromBlock": cur_block, "toBlock": cur_block + BLOCK_STEP}
            )
            filtered_w3_eth_node = self.w3.eth.filter(
                filter_params
            )
            yield filtered_w3_eth_node.get_all_entries()
            cur_block += BLOCK_STEP

    def get_contract_first_block(self, contract):
        return self.w3.eth.getTransactionReceipt(contract)['blockNumber']


    def write_trx_to_csv(self, filename, filter, parse_entry_fn, start_block=None, end_block=None):
        with open(filename, 'w') as out_file:
            csv_writer = csv.writer(out_file, delimiter=',', quotechar='|')
            for entries_batch in self.get_entries_batch(filter, start_block, end_block):
                for entry in entries_batch:
                    csv_writer.writerow(parse_entry_fn(entry))


# Example values in an entry. TODO: Move to readme
# [
# AttributeDict(
# {'address': '0x60F80121C31A0d46B5279700f9DF786054aa5eE5',
# 'blockHash': HexBytes('0x259f9332097c2e6e18072aab455a26442928151867b79486a8280a0b65ec964f'),
# 'blockNumber': 10149090,
# 'data': '0x',
# 'logIndex': 80,
# 'removed': False,
# 'topics': [
# HexBytes('0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef'),
# HexBytes('0x0000000000000000000000000000000000000000000000000000000000000000'),
# HexBytes('0x000000000000000000000000e4c33e64a006f286b6b831cf468f7f5d50ffeac5'),
# HexBytes('0x0000000000000000000000000000000000000000000000000000000000000003')],
# 'transactionHash': HexBytes('0xd15c6fdd8e52aa26b9e9bb1927dd0ba597d17d5f1a85d9addc107d53084d9148'),
# 'transactionIndex': 39}
# ),

def parse_address(address):
    return address.hex()[-40:]

def parse_rari_entry(entry):
    # The topics contains the parameters passed into the function. For the RARI token, we're looking at Transfer() function calls.
    # Transfer (index_topic_1 address from, index_topic_2 address to, index_topic_3 uint256 tokenId)
    _from = parse_address(entry.topics[1])
    to = parse_address(entry.topics[2])
    tokenId = int(entry.topics[3].hex()[2:], base=16)
    return [_from, to, tokenId]

if __name__ == "__main__":
    w3 = W3Eth(ETH_ENDPOINT)

    rari_filter = {
        "topics": [Web3.keccak(text="Transfer(address,address,uint256)").hex()],
        "address": Web3.toChecksumAddress(RARI_CONTRACT),
    }

    w3.write_trx_to_csv(
        filename='rari_transactions.csv',
        filter=rari_filter,
        parse_entry_fn=parse_rari_entry,
        start_block=10149090,
        end_block=10149091,
    )