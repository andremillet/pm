#!/bin/bash

# This script runs the 'configure' command for the 'pm' tool.
# It uses 'poetry run' to ensure the command is executed within the project's virtual environment.

echo "🚀 Launching the 'pm' configuration tool..."
echo "Please enter your GitHub username and Personal Access Token when prompted."

# The full path to poetry is used to avoid PATH issues.
/home/woulschneider/.local/bin/poetry run pm configure
