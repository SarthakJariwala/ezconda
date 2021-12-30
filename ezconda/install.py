import typer
import time
from typing import List, Optional
from pathlib import Path
from conda.cli.python_api import Commands
from conda.cli.python_api import run_command

from .console import console
from ._utils import (
    get_validate_file_name,
    read_env_file,
    add_pkg_to_dependencies,
    write_env_file,
    add_new_channel_to_env_specs,
)
from .experimental import write_lock_file


def install(
    pkg_name: List[str] = typer.Argument(..., help="Packages to install"),
    env_name: str = typer.Option(
        ..., "--name", "-n", help="Name of the environment to install package into"
    ),
    file: Optional[str] = typer.Option(
        None, "--file", "-f", help="'.yml' file to update with new packages"
    ),
    channel: Optional[str] = typer.Option(
        None, "--channel", "-c", help="Additional channel to search for packages"
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
        time.sleep(0.5)
        file = get_validate_file_name(env_name, file)

        env_specs = read_env_file(file)
        env_specs = add_pkg_to_dependencies(env_specs, pkg_name)
        env_specs = add_new_channel_to_env_specs(env_specs, channel)

        status.update("[magenta]Resolving & Installing packages")
        time.sleep(0.5)

        if not channel:
            stdout, stderr, exit_code = run_command(
                Commands.INSTALL, "-n", env_name, *pkg_name, use_exception_handler=True
            )
        else:
            stdout, stderr, exit_code = run_command(
                Commands.INSTALL,
                "-n",
                env_name,
                "--channel",
                channel,
                *pkg_name,
                use_exception_handler=True,
            )

        if exit_code != 0:
            console.print(f"[red]{str(stdout + stderr)}")
            raise typer.Exit()

        if verbose:
            console.print(f"[yellow]{str(stdout)}")

        console.print(f"[bold green] :rocket: Installed packages in {env_name}")

        status.update(f"[magenta]Writing specifications to {file}")
        time.sleep(0.5)
        write_env_file(env_specs, file)
        console.print(f"[bold green] :floppy_disk: Saved specifications to '{file}'")

        if lock:
            status.update(
                f"[yellow]:warning: EXPERIMENTAL :warning: [magenta]Writing lock file "
            )
            time.sleep(0.5)
            write_lock_file(env_name)
            console.print(
                f"[bold green] :lock: Lock file generated [bold yellow]:warning: EXPERIMENTAL :warning:"
            )

        console.print(f"[bold green] :star: Done!")
