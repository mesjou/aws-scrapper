#!/bin/bash -e

# go back to root dir
cd "${0%/*}/.."
echo "Updating requirements..."

# activate venv if necessary
if [[ -z "$VIRTUAL_ENV" ]]; then
    echo "No VIRTUAL_ENV set"
    source venv/bin/activate
else
    echo "VIRTUAL_ENV is set"
fi

# install requirements
pip-compile requirements.in
pip3 install -r requirements.txt

# activate precommit hooks
pre-commit install
pre-commit autoupdate
