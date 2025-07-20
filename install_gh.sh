#!/bin/bash

# Script to install the GitHub CLI (gh) on Debian-based systems (like Ubuntu, Pop!_OS)

set -e # Exit immediately if a command exits with a non-zero status.

# 1. Check if gh is already installed
if command -v gh &> /dev/null
then
    echo "GitHub CLI (gh) is already installed. Version: $(gh --version)"
    echo "You can proceed to the next step: gh auth login"
    exit 0
fi

# 2. Install dependencies and add the repository
echo "GitHub CLI not found. Starting installation..."

(type -p wget >/dev/null || (sudo apt-get update && sudo apt-get install -y wget)) \
&& sudo mkdir -p -m 755 /etc/apt/keyrings \
&& wget -qO- https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo tee /etc/apt/keyrings/githubcli-archive-keyring.gpg > /dev/null \
&& sudo chmod go+r /etc/apt/keyrings/githubcli-archive-keyring.gpg \
&& echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null

# 3. Install gh
echo "Updating package list and installing gh..."
sudo apt-get update
sudo apt-get install -y gh

echo ""
echo "✅ GitHub CLI (gh) installed successfully!"
echo ""
echo "Next step is to authenticate with your GitHub account."
echo "Please run the following command and follow the instructions:"
echo ""
echo "   gh auth login"
