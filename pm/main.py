import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
import json
from pathlib import Path
import requests

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

    for project in projects:
        desc = project.get('description') or 'No description'
        last_synced = project.get('last_synced') or 'Never'
        table.add_row(
            str(project['id']),
            project['name'],
            desc,
            last_synced
        )

    console.print(table)

@app.command()
def show(project_id: int = typer.Argument(..., help="The ID of the project to show.")):
    """
    Show details of a specific project.
    """
    data = load_data()
    projects = data.get("projects", [])

    project = next((p for p in projects if p["id"] == project_id), None)

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
    projects = data.get("projects", [])

    project = next((p for p in projects if p["id"] == project_id), None)

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


if __name__ == "__main__":
    app()