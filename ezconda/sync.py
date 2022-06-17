import subprocess
import typer
import sys
import platform
from typing import Optional
from pathlib import Path
from enum import Enum

from .console import console
from ._utils import get_validate_file_name
from .solver import Solver
from .config import get_default_solver
from .summary import get_summary_for_revision
from .experimental import write_lock_file
from .recreate import read_lock_file_and_install


class SyncFile(str, Enum):
    specfile = "specfile"
    lockfile = "lockfile"


def sync(
    env_name: str = typer.Option(
        ...,
        "--name",
        "-n",
        prompt="Name of the local environment to sync",
        help="Name of the local environment to sync",
    ),
    sync_with: SyncFile = typer.Option(
        ...,
        "--with",
        prompt=True,
        help="Sync environment with either lock file or specifications file",
    ),
    file: Optional[Path] = typer.Option(
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
    Sync local environment with changes made to environment specifications file ('yml') or lockfile.

    Syncing local environment with specifications file will update existing lockfile.
    """

    if solver is None:
        solver = get_default_solver()

    if sync_with == SyncFile.lockfile:
        
        if file is None:
            file = Path(f"{env_name}-{sys.platform}-{platform.machine()}.lock")
        
        read_lock_file_and_install(file, solver, verbose, env_name)

        console.print(
            f"[bold green] :arrows_counterclockwise: '{env_name}' & '{file}' are now in sync!"
        )

        console.print(f"[bold green] :star: Done!")

    else:
        with console.status(f"[magenta]Validating environment and file") as status:

            file = get_validate_file_name(env_name, file)

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
                f"[bold green] :arrows_counterclockwise: '{env_name}' & '{file}' are now in sync!"
            )

            if lock:
                status.update(f"[magenta]Writing lock file")
                write_lock_file(env_name)

            console.print(f"[bold green] :star: Done!")

            if summary:
                get_summary_for_revision(env_name)
