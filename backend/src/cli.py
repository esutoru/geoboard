import typer
import uvicorn

from backend.src.users.cli import app as user_app

app = typer.Typer()
app.add_typer(user_app, name="user")


@app.callback()
def callback() -> None:
    pass


@app.command("run-server")
def run_server(
    host: str = "localhost",
    port: int = 8000,
    log_level: str = "debug",
    reload: bool = True,
) -> None:
    """Run fast api project."""
    uvicorn.run("backend.src.main:app", host=host, port=port, log_level=log_level, reload=reload)
