#!/bin/bash -e

# go back to root dir
cd "${0%/*}/.."

echo "Updating requirements..."

if [[ -z "$VIRTUAL_ENV" ]]; then
    echo "No VIRTUAL_ENV set"
    source venv/bin/activate
else
    echo "VIRTUAL_ENV is set"
fi

pip-compile requirements.in
pip3 install -r requirements.txt
