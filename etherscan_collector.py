from etherscan import Etherscan

API_KEY = 'UYZSHJQ1JZCCQ9VRCSTSYVCV8P9G17DM8Z'
OPENSEA_CONTRACT = '0x7be8076f4ea4a4ad08075c2508e481d6c946d12b'

eth = Etherscan(API_KEY)

transactions = eth.get_internal_txs_by_address(OPENSEA_CONTRACT, startblock=12_265_175, endblock=12_265_175, sort='asc')
print(transactions)
