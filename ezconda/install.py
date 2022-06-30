import subprocess
import typer
from typing import List, Optional
from pathlib import Path

from .console import console
from ._utils import (
    get_validate_file_name,
    read_env_file,
    add_pkg_to_dependencies,
    write_env_file,
    add_new_channel_to_env_specs,
    run_command,
)
from .solver import Solver
from .config import get_default_solver
from .summary import get_summary_for_revision
from .experimental import write_lock_file


def install(
    pkg_name: List[str] = typer.Argument(..., help="Packages to install"),
    env_name: str = typer.Option(
        ...,
        "--name",
        "-n",
        prompt="Name of the environment to install in",
        help="Name of the environment to install package into",
    ),
    file: Optional[str] = typer.Option(
        None, "--file", "-f", help="'.yml' file to update with new packages"
    ),
    channel: Optional[str] = typer.Option(
        None, "--channel", "-c", help="Additional channel to search for packages"
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
    Install package/s in specified conda environment.

    This command will also update the environment file and lock file.
    """

    with console.status(f"[magenta]Validating file, packages, channels") as status:

        file = get_validate_file_name(env_name, file)

        env_specs = read_env_file(file)
        env_specs = add_pkg_to_dependencies(env_specs, pkg_name)
        env_specs = add_new_channel_to_env_specs(env_specs, channel)

        if solver is None:
            solver = get_default_solver()

        status.update(f"[magenta]Resolving & Installing packages using {solver.value}")

        if not channel:
            cmd = [f"{solver.value}", "install", "-n", env_name, *pkg_name, "-y"]
        else:
            cmd = [
                f"{solver.value}",
                "install",
                "-n",
                env_name,
                "--channel",
                channel,
                *pkg_name,
                "-y",
            ]

        run_command(cmd, verbose=verbose)

        console.print(f"[bold green] :rocket: Installed packages in {env_name}")

        status.update(f"[magenta]Writing specifications to {file}")

        write_env_file(env_specs, file)
        console.print(f"[bold green] :floppy_disk: Updated specifications to '{file}'")

        if lock:
            status.update(f"[magenta]Writing lock file")

            write_lock_file(env_name)

        console.print(f"[bold green] :star: Done!")

        if summary:
            get_summary_for_revision(env_name)
