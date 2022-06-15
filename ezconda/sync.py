import subprocess
import typer
from typing import Optional

from .console import console
from ._utils import get_validate_file_name
from .solver import Solver
from .config import get_default_solver
from .summary import get_summary_for_revision
from .experimental import write_lock_file


def sync(
    env_name: str = typer.Option(
        ...,
        "--name",
        "-n",
        prompt="Name of the local environment to sync",
        help="Name of the local environment to sync",
    ),
    file: Optional[str] = typer.Option(
        None,
        "--file",
        "-f",
        help="Environment '.yml' file to use for syncing local environment",
    ),
    solver: Solver = typer.Option(None, help="Solver to use", case_sensitive=False),
    summary: bool = typer.Option(
        True, "--summary", help="Show summary of changes made"
    ),
    verbose: Optional[bool] = typer.Option(
        False, "--verbose", "-v", help="Display standard output from conda"
    ),
    lock: Optional[bool] = typer.Option(True, help="Write lockfile"),
):
    """
    Sync local environment with conda-environment 'yml' file.

    Changes made to the environment yml file will be reflected in the local environment.
    """

    with console.status(f"[magenta]Validating environment and file") as status:

        file = get_validate_file_name(env_name, file)

        if solver is None:
            solver = get_default_solver()

        status.update(
            f"[magenta]Syncing local environment '{env_name}' with file '{file}'"
        )

        p = subprocess.run(
            [
                f"{solver.value}",
                "env",
                "update",
                "-n",
                env_name,
                "--file",
                file,
                "--prune",
            ],
            capture_output=True,
            text=True,
        )

        if p.returncode != 0:
            console.print(f"[red]{str(p.stdout + p.stderr)}")
            raise typer.Exit()

        if verbose:
            console.print(f"[yellow]{str(p.stdout)}")

        console.print(
            "[bold green] :arrows_counterclockwise: Environment & specifications file are now in sync!"
        )

        if lock:
            status.update(f"[magenta]Writing lock file")
            write_lock_file(env_name)

        console.print(f"[bold green] :star: Done!")

        if summary:
            get_summary_for_revision(env_name)
