import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
import json
from pathlib import Path
import requests
from datetime import datetime, timezone

app = typer.Typer(help="🚀 pm: Your intelligent project manager!")
console = Console()

# Define paths
CONFIG_DIR = Path.home() / ".pm"
CONFIG_FILE = CONFIG_DIR / "config.json"
DATA_FILE = CONFIG_DIR / "data.json"

# --- Configuration and Data Loading ---

def ensure_config_exists():
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    if not DATA_FILE.exists():
        with open(DATA_FILE, "w") as f:
            json.dump({"projects": []}, f, indent=4)

def load_config():
    if not CONFIG_FILE.exists():
        console.print("❌ [bold red]Configuration not found.[/bold red] Please run `pm configure` first.")
        raise typer.Exit(1)
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)

def load_data():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def find_project_by_id(project_id: int, data: dict):
    return next((p for p in data.get("projects", []) if p["id"] == project_id), None)

def check_wiki_exists(github_url: str, token: str) -> bool:
    """
    Checks if a GitHub repository has an active Wiki.
    """
    # GitHub Wiki URLs are typically repo_url + ".wiki.git"
    # To check for existence, we can try to fetch the raw Home.md
    # This is a bit hacky, as GitHub doesn't provide a direct API for Wiki existence.
    # A 200 status code for Home.md usually means the Wiki is active.
    
    # Extract owner and repo name from github_url
    parts = github_url.split('/')
    owner = parts[-2]
    repo_name = parts[-1].replace(".git", "") # Remove .git if present

    wiki_raw_url = f"https://raw.githubusercontent.com/wiki/{owner}/{repo_name}/Home.md"
    headers = {"Authorization": f"token {token}"}

    try:
        response = requests.head(wiki_raw_url, headers=headers, allow_redirects=True)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

# --- Typer App ---

@app.callback(invoke_without_command=True)
def cli_main(ctx: typer.Context):
    ensure_config_exists()
    if ctx.invoked_subcommand is None:
        console.print("🚀 Welcome to [bold green]pm[/bold green] - your intelligent project manager!")
        console.print("Use [cyan]pm --help[/cyan] to see available commands.")

@app.command()
def configure():
    """
    Configure your GitHub username and Personal Access Token (PAT).
    """
    ensure_config_exists()
    console.print("🔑 Configuring GitHub credentials...")
    username = typer.prompt("Enter your GitHub username")
    token = typer.prompt("Enter your GitHub Personal Access Token (PAT)", hide_input=True)
    config_data = {"github_username": username, "github_pat": token}
    with open(CONFIG_FILE, "w") as f:
        json.dump(config_data, f, indent=4)
    console.print(f"✅ Configuration saved successfully to [cyan]{CONFIG_FILE}[/cyan]")

@app.command(name="import")
def import_projects():
    """
    Import repositories from your GitHub account.
    """
    config = load_config()
    data = load_data()
    username = config["github_username"]
    token = config["github_pat"]

    console.print(f"🔎 Fetching repositories for user [bold blue]{username}[/bold blue]...")
    
    headers = {"Authorization": f"token {token}"}
    url = f"https://api.github.com/user/repos?type=owner&sort=updated"
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status() # Raises an exception for bad status codes
        repos = response.json()

        tracked_repos = {p['name'] for p in data['projects']}
        new_projects_added = 0

        for repo in repos:
            repo_name = repo["name"]
            if repo_name in tracked_repos:
                continue # Skip already tracked projects

            track = typer.confirm(f"Track repository [bold green]{repo_name}[/bold green]?", default=False)
            if track:
                new_project = {
                    "id": len(data['projects']) + 1,
                    "name": repo_name,
                    "github_url": repo["html_url"],
                    "description": repo["description"],
                    "last_synced": None,
                    "tasks": []
                }
                data['projects'].append(new_project)
                tracked_repos.add(repo_name)
                new_projects_added += 1

        if new_projects_added > 0:
            save_data(data)
            console.print(f"✨ Successfully added {new_projects_added} new project(s)!")
        else:
            console.print("No new projects were added.")

    except requests.exceptions.RequestException as e:
        console.print(f"❌ [bold red]Error fetching repositories:[/bold red] {e}")
        raise typer.Exit(1)

@app.command(name="list")
def list_projects():
    """
    List all tracked projects.
    """
    config = load_config() # Load config to get token for wiki check
    token = config["github_pat"]

    data = load_data()
    projects = data.get("projects", [])

    if not projects:
        console.print("🤷 No projects are being tracked yet. Use `pm import` to add some!")
        return

    table = Table(title="Tracked Projects")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Name", style="green")
    table.add_column("Description")
    table.add_column("Last Synced", style="magenta")
    table.add_column("Wiki", style="blue") # New column for Wiki status

    for project in projects:
        desc = project.get('description') or 'No description'
        last_synced = project.get('last_synced') or 'Never'
        
        wiki_status = "N/A"
        if project.get('github_url'):
            if check_wiki_exists(project['github_url'], token):
                wiki_status = "✅ Yes"
            else:
                wiki_status = "❌ No"

        table.add_row(
            str(project['id']),
            project['name'],
            desc,
            last_synced,
            wiki_status
        )

    console.print(table)

@app.command()
def show(project_id: int = typer.Argument(..., help="The ID of the project to show.")):
    """
    Show details of a specific project.
    """
    data = load_data()
    project = find_project_by_id(project_id, data)

    if project is None:
        console.print(f"❌ [bold red]Project with ID {project_id} not found.[/bold red]")
        raise typer.Exit(1)

    console.print(Panel(
        Text(f"ID: {project.get('id')}\n") +
        Text(f"Name: {project.get('name')}\n") +
        Text(f"GitHub URL: {project.get('github_url')}\n") +
        Text(f"Description: {project.get('description') or 'No description'}\n") +
        Text(f"Last Synced: {project.get('last_synced') or 'Never'}\n") +
        Text("\nTasks:", style="bold"),
        title=f"Project: [bold green]{project.get('name')}[/bold green]",
        border_style="blue"
    ))

    tasks = project.get("tasks", [])
    if tasks:
        task_table = Table(title="Tasks")
        task_table.add_column("ID", style="cyan")
        task_table.add_column("Description", style="white")
        task_table.add_column("Status", style="yellow")

        for task in tasks:
            task_table.add_row(
                str(task["id"]),
                task["description"],
                task["status"]
            )
        console.print(task_table)
    else:
        console.print("🤷 No tasks for this project yet.")

@app.command(name="add-task")
def add_task(
    project_id: int = typer.Argument(..., help="The ID of the project to add the task to."),
    description: str = typer.Argument(..., help="The description of the task.")
):
    """
    Add a new task to a project.
    """
    data = load_data()
    project = find_project_by_id(project_id, data)

    if project is None:
        console.print(f"❌ [bold red]Project with ID {project_id} not found.[/bold red]")
        raise typer.Exit(1)

    tasks = project.get("tasks", [])
    new_task_id = max([t["id"] for t in tasks]) + 1 if tasks else 1

    new_task = {
        "id": new_task_id,
        "description": description,
        "status": "todo"
    }
    tasks.append(new_task)
    project["tasks"] = tasks # Ensure the tasks list is updated in the project dict

    save_data(data)
    console.print(f"✅ Task '[bold green]{description}[/bold green]' added to project '[bold blue]{project['name']}[/bold blue]' (ID: {project_id}).")

@app.command(name="update-task")
def update_task(
    task_id: int = typer.Argument(..., help="The ID of the task to update."),
    status: str = typer.Option(..., "--status", "-s", help="The new status of the task (todo, doing, done).")
):
    """
    Update the status of a task.
    """
    data = load_data()
    projects = data.get("projects", [])

    found_task = False
    for project in projects:
        tasks = project.get("tasks", [])
        for task in tasks:
            if task["id"] == task_id:
                # Validate status
                valid_statuses = ["todo", "doing", "done"]
                if status not in valid_statuses:
                    console.print(f"❌ [bold red]Invalid status: {status}.[/bold red] Valid statuses are: {', '.join(valid_statuses)}.")
                    raise typer.Exit(1)

                task["status"] = status
                found_task = True
                break
        if found_task:
            break

    if not found_task:
        console.print(f"❌ [bold red]Task with ID {task_id} not found.[/bold red]")
        raise typer.Exit(1)

    save_data(data)
    console.print(f"✅ Task [bold cyan]{task_id}[/bold cyan] updated to status '[bold green]{status}[/bold green]'.")

@app.command()
def sync(
    project_id: int = typer.Argument(..., help="The ID of the project to sync.")
):
    """
    Syncs a project with its GitHub repository, fetching new commits and storing them.
    Summarization is a future feature.
    """
    config = load_config()
    data = load_data()
    project = find_project_by_id(project_id, data)

    if project is None:
        console.print(f"❌ [bold red]Project with ID {project_id} not.[/bold red]")
        raise typer.Exit(1)

    console.print(f"🔄 Syncing project [bold blue]{project['name']}[/bold blue]...")

    username = config["github_username"]
    token = config["github_pat"]
    repo_name = project["name"]
    owner = username # Assuming the user is the owner for now

    headers = {"Authorization": f"token {token}"}
    
    # Get the last synced date to fetch only new commits
    last_synced_dt = None
    if project["last_synced"]:
        last_synced_dt = datetime.fromisoformat(project["last_synced"])
        if last_synced_dt.tzinfo is None: # If it's naive, assume UTC and make it aware
            last_synced_dt = last_synced_dt.replace(tzinfo=timezone.utc)
        else: # If it's already aware, convert to UTC
            last_synced_dt = last_synced_dt.astimezone(timezone.utc)

    # Fetch commits from GitHub API
    commits_url = f"https://api.github.com/repos/{owner}/{repo_name}/commits"
    
    try:
        response = requests.get(commits_url, headers=headers)
        response.raise_for_status()
        commits = response.json()

        new_commits_data = []
        for commit in commits:
            commit_date_str = commit["commit"]["author"]["date"]
            # Replace 'Z' with '+00:00' for proper ISO 8601 parsing
            commit_dt = datetime.fromisoformat(commit_date_str.replace("Z", "+00:00"))
            
            if last_synced_dt and commit_dt <= last_synced_dt:
                continue # Skip old commits
            
            # Fetch full commit details including diff
            commit_detail_url = commit["url"]
            detail_response = requests.get(commit_detail_url, headers=headers)
            detail_response.raise_for_status()
            commit_details = detail_response.json()
            
            new_commits_data.append({
                "sha": commit["sha"],
                "message": commit["commit"]["message"],
                "author": commit["commit"]["author"]["name"],
                "date": commit_date_str,
                "diff": commit_details.get("files", []) # Diff is in 'files' array
            })
        
        if not new_commits_data:
            console.print("✅ No new commits to sync.")
            project["last_synced"] = datetime.now(timezone.utc).isoformat()
            save_data(data)
            return

        # Sort new commits by date ascending
        new_commits_data.sort(key=lambda x: datetime.fromisoformat(x["date"].replace("Z", "+00:00")))

        # Store raw commit data in sync_logs
        if "sync_logs" not in project:
            project["sync_logs"] = []
        
        # Append each new commit as a separate log entry
        for commit_data in new_commits_data:
            project["sync_logs"].append({
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "commit_sha": commit_data["sha"],
                "message": commit_data["message"],
                "author": commit_data["author"],
                "date": commit_data["date"],
                "diff": commit_data["diff"],
                "summary": "(Summary to be generated later)" # Placeholder for future summarization
            })

        project["last_synced"] = datetime.now(timezone.utc).isoformat()
        save_data(data)

        console.print(f"✅ Project [bold blue]{project['name']}[/bold blue] synced successfully! {len(new_commits_data)} new commits stored.")

    except requests.exceptions.RequestException as e:
        console.print(f"❌ [bold red]Error syncing project:[/bold red] {e}")
        raise typer.Exit(1)

@app.command(name="new")
def new_project(
    project_name: str = typer.Argument(..., help="The name of the new project."),
    description: str = typer.Option("", "--description", "-d", help="A brief description of the new project."),
    public: bool = typer.Option(True, "--public", "-p", help="Make the new GitHub repository public.")
):
    """
    Creates a new project, including a GitHub repository, and tracks it with pm.
    """
    config = load_config()
    data = load_data()
    username = config["github_username"]
    token = config["github_pat"]

    console.print(f"✨ Creating new project [bold green]{project_name}[/bold green]...")

    # 1. Create GitHub Repository
    repo_creation_url = "https://api.github.com/user/repos"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    payload = {
        "name": project_name,
        "description": description,
        "private": not public,
        "has_wiki": True # Always enable Wiki for new projects
    }

    try:
        response = requests.post(repo_creation_url, headers=headers, json=payload)
        response.raise_for_status()
        repo_data = response.json()
        github_url = repo_data["html_url"]
        console.print(f"✅ GitHub repository created: [link={github_url}]{github_url}[/link]")

    except requests.exceptions.RequestException as e:
        console.print(f"❌ [bold red]Error creating GitHub repository:[/bold red] {e}")
        # Print the full response text for debugging
        if response.text:
            console.print(f"Response: {response.text}")
        raise typer.Exit(1)

    # 2. Add project to pm's data
    new_project_id = max([p["id"] for p in data["projects"]]) + 1 if data["projects"] else 1
    new_project_entry = {
        "id": new_project_id,
        "name": project_name,
        "github_url": github_url,
        "description": description,
        "last_synced": None,
        "tasks": [],
        "sync_logs": []
    }
    data["projects"].append(new_project_entry)
    save_data(data)

    console.print(f"✅ Project [bold green]{project_name}[/bold green] (ID: {new_project_id}) added to pm tracking.")
    console.print("💡 Remember to initialize a local Git repository and link it to your new GitHub repo if you plan to develop locally.")


if __name__ == "__main__":
    app()
