#!/bin/bash

# add the project dir to PYTHONPATH
curr_dir=$(pwd)
echo "${curr_dir}"
export PYTHONPATH=${PYTHONPATH}:${curr_dir}

# source env vars from .env file
echo "Sourcing environment variables ..."
set -a
. .env
set +a
echo "Done!"

echo

# start project
echo "Starting local environment ..."

# Create a venv in the current directory if does not exist
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
# Activate the venv
. venv/bin/activate
# Upgrade pip and install pip-tools
pip install pip pip-tools --upgrade
# Install the required modules in your environment
pip-sync

# Initiate a database
echo "Initiating database ..."
#python init.py

echo "Done!"
