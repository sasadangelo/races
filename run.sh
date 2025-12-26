#!/bin/bash

# Activate virtual environment if it exists
if [ -d ".venv" ]; then
    source .venv/bin/activate
fi

# Set Flask app
export FLASK_APP=races

# Run Flask with configuration from config.yml
python -c "
from app.core import settings
import os
import sys

# Get configuration values
host = settings.app.host
port = settings.app.port
debug = '--debug' if settings.app.debug else ''

# Run Flask
cmd = f'flask run --host={host} --port={port} {debug}'
print(f'Starting Flask app: {cmd}')
os.system(cmd)
"
