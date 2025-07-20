# `pm` - The Intelligent Project Manager

`pm` is a command-line interface (CLI) tool designed to be an intelligent development assistant. It helps you document, track, and manage your project ideas by integrating with Git and GitHub to automate progress tracking.

This project is being developed using its own logic, serving as the first project managed by `pm` itself.

## Core Features

- **GitHub Integration**: Configure `pm` with your GitHub credentials to manage repositories.
- **Project Tracking**: Add existing repositories or create new ones to track.
- **Automated Sync**: Fetch new commits from GitHub and store their details (messages, diffs) for later analysis.
- **Task Management**: Add and update tasks for your projects.
- **Intelligent Summaries**: (Future) Automatically generate concise summaries of project progress based on synced commits.
- **Local LLM Support**: (Future) Option to use a local language model for privacy and offline capabilities.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/andremillet/pm.git
    cd pm
    ```

2.  **Install Poetry (if you haven't already):**
    ```bash
    curl -sSL https://install.python-poetry.org | python3 -
    ```

3.  **Install project dependencies:**
    ```bash
    poetry install
    ```

## Usage

All `pm` commands should be run using `poetry run pm <command> [arguments]`. This ensures the application runs within its isolated Python environment with all necessary dependencies.

### `pm configure`

Configures your GitHub username and Personal Access Token (PAT). This is required for `pm` to interact with your GitHub repositories.

```bash
./run_configure.sh
```

Follow the prompts to enter your GitHub username and PAT. You can generate a PAT [here](https://github.com/settings/tokens/new) (ensure it has `repo` permissions).

### `pm import`

Interactively imports repositories from your GitHub account, allowing you to select which ones `pm` should track.

```bash
./run_import.sh
```

### `pm list`

Lists all projects currently being tracked by `pm`.

```bash
poetry run pm list
```

### `pm show <project_id>`

Shows detailed information about a specific project, including its tasks and (future) sync logs.

```bash
poetry run pm show 1 # Replace 1 with the actual project ID
```

### `pm add-task <project_id> "<task_description>"`

Adds a new task to a specified project.

```bash
poetry run pm add-task 1 "Implement the sync command"
```

### `pm update-task <task_id> --status <status>`

Updates the status of a specific task. Valid statuses are `todo`, `doing`, and `done`.

```bash
poetry run pm update-task 1 --status doing
```

### `pm sync <project_id>`

Syncs a project with its GitHub repository. This command fetches new commits and stores their details (SHA, message, author, date, and diffs) in `pm`'s internal data. Intelligent summarization of these commits is a planned future feature.

```bash
poetry run pm sync 1 # Replace 1 with the actual project ID
```

---
*This README is actively being developed alongside the project.*