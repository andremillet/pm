import typer
from rich.console import Console

app = typer.Typer()
console = Console()

@app.command()
def main():
    """
    Displays a welcome message.
    """
    console.print("🚀 Welcome to [bold green]pm[/bold green] - your intelligent project manager!")
    console.print("Use [cyan]pm --help[/cyan] to see available commands.")

if __name__ == "__main__":
    app()