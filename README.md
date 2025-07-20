# `pm` - The Intelligent Project Manager

`pm` is a command-line interface (CLI) tool designed to be an intelligent development assistant. It helps you document, track, and manage your project ideas by integrating with Git and GitHub to automate progress tracking.

This project is being developed using its own logic, serving as the first project managed by `pm` itself.

## Core Features

- **GitHub Integration**: Configure `pm` with your GitHub credentials to manage repositories.
- **Project Tracking**: Add existing repositories or create new ones to track.
- **Automated Summaries**: (Future) Automatically generate progress summaries from `git` logs.
- **Local LLM Support**: (Future) Option to use a local language model for privacy and offline use.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/andremillet/pm.git
    cd pm
    ```

2.  **Install dependencies using Poetry:**
    ```bash
    # Install Poetry if you haven't already
    curl -sSL https://install.python-poetry.org | python3 -
    
    # Install project dependencies
    poetry install
    ```

## Usage

1.  **Configure your credentials:**

    Run the configuration script and follow the prompts:
    ```bash
    ./run_configure.sh
    ```

2.  **See available commands:**
    ```bash
    poetry run pm --help
    ```

---
*This README is actively being developed alongside the project.*

**Added a new line to trigger a new commit for testing sync command.**