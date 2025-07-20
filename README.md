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

### 1. Using the `install.sh` script (Recommended for Users)

This is the easiest way to get `pm` installed on your Linux or macOS system. It downloads the latest alpha release from GitHub and installs it using `pip`.

```bash
curl -sSL https://raw.githubusercontent.com/andremillet/pm/master/install.sh | bash
```

After installation, you will need to configure your GitHub credentials:

```bash
pm configure
```

### 2. For Developers (using Poetry)

If you plan to contribute to `pm` or want to manage its dependencies with Poetry:

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

4.  **Configure `pm` with your GitHub credentials:**
    This step is crucial for `pm` to interact with your GitHub account.
    ```bash
    ./run_configure.sh
    ```
    Follow the prompts to enter your GitHub username and PAT.

### 3. For Users (via pip from GitHub Release)

Once a release is available, you can install `pm` directly using `pip`.

1.  **Install `pm`:**
    ```bash
    pip install https://github.com/andremillet/pm/releases/download/v0.1.0-alpha/pm-0.1.0-py3-none-any.whl
    ```

2.  **Configure `pm`:**
    After installation, run the configuration script:
    ```bash
    pm configure
    ```
    Follow the prompts to enter your GitHub username and PAT.

## Usage

### For Developers (using Poetry)

During development, always run `pm` commands using `poetry run` to ensure it uses the correct isolated environment:

```bash
poetry run pm <command> [arguments]
```

For example:

```bash
poetry run pm list
```

### For Users (after pip installation or install.sh)

After installing via `pip` or `install.sh`, you can run `pm` commands directly:

```bash
pml <command> [arguments]
```

For example:

```bash
pm list
```

### `pm configure`

Configures your GitHub username and Personal Access Token (PAT). This is a prerequisite for most `pm` functionalities.

```bash
./run_configure.sh
```

Follow the prompts to enter your GitHub username and PAT. You can generate a PAT [here](https://github.com/settings/tokens/new) (ensure it has `repo` scope).

### `pm import`

Interactively imports repositories from your GitHub account, allowing you to select which ones `pm` should track.

```bash
./run_import.sh
```

### `pm list`

Lists all projects currently being tracked by `pm`, including their ID, name, description, last sync date, and Wiki status.

```bash
poetry run pm list
```

### `pm show <project_id>`

Shows detailed information about a specific project, including its tasks and raw sync logs.

```bash
poetry run pm show 1 # Replace 1 with the actual project ID
```

### `pm add-task <project_id> "<task_description>"`

Adds a new task to a specified project. The task will have a default status of `todo`.

```bash
poetry run pm add-task 1 "Implement the sync command"
```

### `pm update-task <task_id> --status <status>`

Updates the status of a specific task. Valid statuses are `todo`, `doing`, and `done`.

```bash
poetry run pm update-task 1 --status doing
```

### `pm sync <project_id>`

Syncs a project with its GitHub repository. This command fetches new commits and stores their details (SHA, message, author, date, and diffs) in `pm`'s internal data (`~/.pm/data.json`). Intelligent summarization of these commits is a planned future feature that will leverage LLMs.

```bash
poetry run pm sync 1 # Replace 1 with the actual project ID
```

### `pm new <project_name>`

Creates a new project, including a GitHub repository (public by default, with Wiki enabled), and adds it to `pm`'s tracking.

```bash
poetry run pm new my-new-project -d "A fantastic new idea" --public
```

### Options

*   `-d, --description <description>`: A brief description for the new project and GitHub repository.
*   `-p, --public`: Make the new GitHub repository public (default: `True`). Use `--no-public` to create a private repository.

---
*This README is actively being developed alongside the project.*