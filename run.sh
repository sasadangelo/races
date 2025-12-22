#!/bin/bash

# Activate virtual environment if it exists
if [ -d ".venv" ]; then
    source .venv/bin/activate
fi

# Set Flask app and run in debug mode
export FLASK_APP=races
flask run --debug

# Made with Bob
