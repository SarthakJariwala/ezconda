import typer

from . import __version__
from .console import console

from .tree import show
from .create import create
from .install import install
from .remove import remove


app = typer.Typer()

app.command()(create)
app.command()(install)
app.command()(remove)
app.command()(show)


@app.command()
def version():
    """Shows the version of 'ezconda' installed"""
    console.print(f"[magenta]{__version__}")
