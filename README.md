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

## On-chain data

