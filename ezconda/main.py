import typer

from . import __version__
from .console import console

# from .tree import show
from .create import create
from .install import install
from .remove import remove
from .recreate import recreate
from .experimental.lock import lock


app = typer.Typer(
    help="Create, Manage, Re-create conda environments & specifications with ease"
)

app.command()(create)
app.command()(install)
app.command()(remove)
app.command()(recreate)
app.command()(lock)
# app.command()(show)


@app.command()
def version():
    """Shows the version of 'ezconda' installed"""
    console.print(f"[magenta]{__version__}")
