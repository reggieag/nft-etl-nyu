# nft-etl-nyu

## Setup
We use poetry to manage dependencies and virtual environments.

Install poetry based on their documentation.
https://python-poetry.org/docs/

On Unix you can execute this command:
```bash
curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python
source $HOME/.poetry/env
```

Then install the python packages.
```bash
poetry install --no-root
```

You can now run commands using `poetry run` and you will have access to the packages defined in the `pyproject.toml` file.
```bash
poetry run python
```

## Pulling Down Ethereum Data
To pull down Rari ethereum data
```bash
poetry run python rari_collector.py
```

# Datasets

## Punks Dataset
We look at the CryptoPunks dataset, focusing in on buy transactions. CryptoPunks is one of the most successful NFT projects and was created by larvalabs. CryptoPunks will be auctioned at Christie's for millions of dollars.

In our dataset we focus on by events. Inside the buy events are the buyer address, the seller address, and the total price in ethereum. We also include the block number and transaction id in this dataset. The block id and transaction id can be used to sort events by time.