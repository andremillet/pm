# Project Vision: `pm` - The Intelligent Project Manager

## 1. Overview

`pm` is a command-line interface (CLI) tool designed to be an intelligent development assistant. Its primary goal is to help developers document, track, and manage their project ideas seamlessly, from conception to completion.

The core philosophy is "dogfooding": `pm` will be developed using its own logic and capabilities. It will integrate deeply with Git and GitHub to automate tracking and provide insightful progress summaries.

## 2. Core Features

### Phase 1: Foundation & Manual Tracking
- **`pm configure`**: Securely set up GitHub username and Personal Access Token (PAT).
- **`pm add --repo <url>`**: Add an existing GitHub repository to `pm`. It will clone the repo locally if needed.
- **`pm list`**: List all tracked projects.
- **`pm add-task <project_id> "task description"`**: Manually add a task to a project.
- **`pm update-task <task_id> --status <status>`**: Update a task's status (`todo`, `doing`, `done`).

### Phase 2: GitHub Integration & Automated Import
- **`pm import`**: Interactively fetch and import a user's repositories from GitHub, allowing them to select which ones to track.

### Phase 3: Intelligent Sync & Automated Summarization
- **`pm sync <project_id>`**: The core command. It will:
    1. Fetch the latest changes from the remote repository (`git pull`).
    2. Read the `git log` and `git diff` since the last sync.
    3. **(Magic)** Use a Language Model to generate a concise, human-readable summary of the progress.
    4. Store this summary as a log entry for the project.
- **`pm show <project_id>`**: Display project details, including the automatically generated progress log.

### Phase 4: Local LLM Integration (Future Goal)
- **Modular Summarization Engine**: The summarization logic will be designed as a pluggable module.
- **Local Model Support**: Implement a summarizer that runs on a local, open-source LLM (e.g., using `llama-cpp-python`).
- **User-Selectable Engine**: Allow the user to choose between the API-based engine (e.g., Gemini) and the local engine via a configuration setting. This ensures privacy, offline capability, and zero cost for users who prefer it.

## 3. Technical Stack
- **Language**: Python 3
- **CLI Framework**: Typer
- **API Communication**: `requests`
- **Git Interaction**: `subprocess` module
- **Data Storage**:
    - `~/.pm/data.json`: For project metadata and progress logs.
    - `~/.pm/config.json`: For user configuration (GitHub credentials, summarization engine choice).
