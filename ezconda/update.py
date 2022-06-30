import subprocess
import typer
from typing import Optional
from pathlib import Path

from .console import console
from ._utils import get_validate_file_name, run_command
from .solver import Solver
from .config import get_default_solver
from .summary import get_summary_for_revision
from .experimental import write_lock_file


def update(
    env_name: str = typer.Option(
        ...,
        "--name",
        "-n",
        prompt="Name of the environment to update",
        help="Name of the environment to update",
    ),
    file: Optional[Path] = typer.Option(
        None,
        "--file",
        "-f",
        help="Environment '.yml' file to use for updating environment",
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
    Update environment according to specifications file.
    """
    if solver is None:
        solver = get_default_solver()

    with console.status(f"[magenta]Validating environment and file") as status:

        file = get_validate_file_name(env_name, file)

        status.update(f"[magenta]Updating environment '{env_name}' with file '{file}'")

        cmd = [
            f"{solver.value}",
            "env",
            "update",
            "-n",
            env_name,
            "--file",
            file,
            "--prune",
        ]

        run_command(cmd, verbose=verbose)

        console.print(f"[bold green] :white_heavy_check_mark: '{env_name}' updated!")

        if lock:
            status.update(f"[magenta]Updating lock file")
            write_lock_file(env_name)

        console.print(f"[bold green] :star: Done!")

        if summary:
            get_summary_for_revision(env_name)
