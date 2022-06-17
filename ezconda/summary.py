import json
import subprocess
from textwrap import dedent
import typer

from rich.tree import Tree

from .console import console


def summary(
    name: str = typer.Option(
        ...,
        "--name",
        "-n",
        prompt="Name of the environment",
        help="Name of the environment to summarize",
    ),
    revision: int = typer.Option(
        -1,
        "--revision",
        help="Revision number to summarize; default is latest",
    ),
):
    """
    Show environment summary for the revision number.
    By default, it will show the latest revision.
    """
    _ = get_summary_for_revision(name, revision_no=revision)


def get_summary_for_revision(name: str, revision_no: int = -1):
    """ "
    Get summary for the revision number of the environment.
    By default, it will show the latest revision.
    """

    p = subprocess.run(
        ["conda", "list", "--revision", "-n", name, "--json"],
        capture_output=True,
        text=True,
    )

    # summary info
    _rev_data = json.loads(p.stdout)

    try:
        _info = _rev_data[revision_no]
    except IndexError:
        console.print(
            f"[red]Revision {revision_no} not found.\nYou have {len(_rev_data)} revisions for {name} environment."
        )
        raise typer.Exit(code=1)

    _installed = _info["install"]
    _upgraded = _info["upgrade"]
    _removed = _info["remove"]
    _downgraded = _info["downgrade"]

    console.print(
        dedent(
            f"""
            [bold green]{len(_installed)} Installs,[/] [bold purple]{len(_upgraded)} Upgrades[/], [bold yellow]{len(_downgraded)} Downgrades[/], [bold red]{len(_removed)} Removals[/]
            """
        )
    )

    tree = Tree("[bold]Summary[/]")
    if _installed:
        install_branch = tree.add("[bold green]Installs[/]")
        for i in _installed:
            install_branch.add(f"[green]{i}[/]")
    if _upgraded:
        upgrade_branch = tree.add("[bold purple]Upgrades[/]")
        for u in _upgraded:
            upgrade_branch.add(f"[purple]New: {u['new']}[/]\nOld: {u['old']}")
    if _downgraded:
        downgrade_branch = tree.add("[bold yellow]Downgrades")
        for d in _downgraded:
            downgrade_branch.add(f"[yellow]New: {d['new']}[/]\nOld: {d['old']}")
    if _removed:
        removal_branch = tree.add("[bold red]Removals[/]")
        for r in _removed:
            removal_branch.add(f"[red]{r}[/]")

    if _installed or _upgraded or _downgraded or _removed:
        console.print(tree)
    
    return _installed, _upgraded, _downgraded, _removed
