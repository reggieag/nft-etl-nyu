import csv

from web3 import Web3
from urllib.parse import urlparse

DEFAULT_BLOCK_STEP = 4000


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
            self._w3 = Web3(Web3.WebsocketProvider(self.endpoint))
        elif url.scheme == 'https' or url.scheme == 'http':
            self._w3 = Web3(Web3.HTTPProvider(self.endpoint))
        return self._w3

    def get_entries_batch(self, filter_params, starting_block=None, ending_block=None, block_step=None):
        cur_block = starting_block or 0
        ending_block = ending_block or self.w3.eth.blockNumber
        block_step = block_step or DEFAULT_BLOCK_STEP

        while cur_block <= ending_block:
            filter_params.update(
                {"fromBlock": cur_block, "toBlock": cur_block + block_step}
            )
            filtered_w3_eth_node = self.w3.eth.filter(
                filter_params
            )
            yield filtered_w3_eth_node.get_all_entries()
            cur_block += block_step + 1

    def get_contract_first_block(self, contract):
        return self.w3.eth.getTransactionReceipt(contract)['blockNumber']

    def write_entries_to_csv(self, filename, filter, parse_entry_fn, start_block=None, end_block=None):
        with open(filename, 'w') as out_file:
            csv_writer = csv.writer(out_file, delimiter=',', quotechar='|')
            for entries_batch in self.get_entries_batch(filter, start_block, end_block):
                # transactionIndex is the position of a transaction within a block.
                entries_batch.sort(key=lambda x: (x['blockNumber'], x['transactionIndex']))
                for entry in entries_batch:
                    csv_writer.writerow(parse_entry_fn(entry))


def parse_address(address):
    return address.hex()[-40:]
