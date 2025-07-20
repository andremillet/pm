import typer
from rich.console import Console
import json
from pathlib import Path

app = typer.Typer(help="🚀 pm: Your intelligent project manager!")
console = Console()

# Define the configuration path
CONFIG_DIR = Path.home() / ".pm"
CONFIG_FILE = CONFIG_DIR / "config.json"

def ensure_config_dir_exists():
    """Ensures the configuration directory exists."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)

@app.callback(invoke_without_command=True)
def cli_main(ctx: typer.Context):
    """
    Displays a welcome message if no command is provided.
    """
    if ctx.invoked_subcommand is None:
        console.print("🚀 Welcome to [bold green]pm[/bold green] - your intelligent project manager!")
        console.print("Use [cyan]pm --help[/cyan] to see available commands.")

@app.command()
def configure():
    """
    Configure your GitHub username and Personal Access Token (PAT).
    """
    ensure_config_dir_exists()

    console.print("🔑 Configuring GitHub credentials...")

    username = typer.prompt("Enter your GitHub username")
    # Using hide_input=True for the token
    token = typer.prompt("Enter your GitHub Personal Access Token (PAT)", hide_input=True)

    config_data = {
        "github_username": username,
        "github_pat": token
    }

    with open(CONFIG_FILE, "w") as f:
        json.dump(config_data, f, indent=4)

    console.print(f"✅ Configuration saved successfully to [cyan]{CONFIG_FILE}[/cyan]")


if __name__ == "__main__":
    app()
