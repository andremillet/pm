#!/bin/bash

# This script installs the pm CLI tool.
# It downloads the latest alpha release from GitHub and installs it using pip.

set -e # Exit immediately if a command exits with a non-zero status.

REPO_OWNER="andremillet"
REPO_NAME="pm"
RELEASE_TAG="v0.1.0-alpha" # Update this for new releases
PACKAGE_NAME="pm-0.1.0-py3-none-any.whl" # Update this for new releases

INSTALL_DIR="$HOME/.local/bin"

echo "🚀 Installing pm CLI tool..."

# Check for pip
if ! command -v pip &> /dev/null
then
    echo "❌ pip is not installed. Please install pip first (e.g., sudo apt install python3-pip)."
    exit 1
fi

# Create install directory if it doesn't exist
mkdir -p "$INSTALL_DIR"

# Download the wheel file
DOWNLOAD_URL="https://github.com/$REPO_OWNER/$REPO_NAME/releases/download/$RELEASE_TAG/$PACKAGE_NAME"
TEMP_DIR=$(mktemp -d)
TEMP_WHEEL="$TEMP_DIR/$PACKAGE_NAME"

echo "Downloading $PACKAGE_NAME from $DOWNLOAD_URL..."
curl -L -o "$TEMP_WHEEL" "$DOWNLOAD_URL"

# Install using pip
echo "Installing pm using pip..."
pip install --user "$TEMP_WHEEL"

# Clean up
rm -rf "$TEMP_DIR"

echo "✅ pm installed successfully!"
echo ""
echo "To ensure 'pm' command is available, make sure '$HOME/.local/bin' is in your PATH."
echo "You might need to restart your terminal or run: source ~/.bashrc (or ~/.zshrc)"
echo ""
echo "Next, configure your GitHub credentials:"
echo "   pm configure"
