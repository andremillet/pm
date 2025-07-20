#!/bin/bash

# This script runs the 'import' command for the 'pm' tool.
# It uses 'poetry run' to ensure the command is executed within the project's virtual environment.

echo "🚀 Launching the 'pm' import tool..."
echo "This will fetch your GitHub repositories and ask which ones to track."

# The full path to poetry is used to avoid PATH issues.
/home/woulschneider/.local/bin/poetry run pm import
