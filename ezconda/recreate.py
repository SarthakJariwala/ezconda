import typer
import time
import json
from typing import List, Optional
from pathlib import Path
from conda.cli.python_api import Commands
from conda.cli.python_api import run_command

from .console import console


def read_lock_file_and_install(lock_file: Path, env_name: str, verbose: bool) -> None:
    """
    Reads lock file; identifies packages, their version number and build string and groups them by
    channel and attempts installation.

    If errors are encountered during installation, user is informed.
    """

    with console.status(f"[magenta]Reading lock file") as status:
        time.sleep(0.5)

        with open(lock_file, "r") as f:
            complete_spec = json.load(f)

        # only create environment if lock file load is successful
        status.update(f"[magenta]Creating conda environment {env_name}")
        time.sleep(0.5)
        _ = run_command(Commands.CREATE, "-n", env_name, use_exception_handler=True)

        # find the channels in the lock file
        channels = list(set([d["channel"] for d in complete_spec]))

        for channel in channels:
            # get package-version-build for packages from a channel
            status.update(f"[magenta]Collecting packages for channel : {channel}")
            time.sleep(0.5)
            pvb = [
                f"{d['name']}={d['version']}={d['build_string']}"
                for d in complete_spec
                if d["channel"] == channel
            ]
            status.update(f"[magenta]Installing packages for channel : {channel}")
            time.sleep(0.5)
            stdout, stderr, exit_code = run_command(
                Commands.INSTALL, "-n", env_name, *pvb, "-c", channel
            )

            if verbose:
                console.print(f"[bold yellow]{stdout}")

            if exit_code != 0:
                console.print("[red]" + str(stdout + stderr))
                raise typer.Exit()

            console.print(
                f"[bold green] :check: Installed all packages from channel : {channel}",
            )

        console.print(
            f"[bold green] :rocket: Installed all dependencies from '{lock_file}'!"
        )


def recreate(
    file: str = typer.Argument(
        ..., help="Lock file to use to re-create an environment"
    ),
    name: Optional[str] = typer.Option(
        None,
        "--name",
        "-n",
        help="Name of the environment to create",
    ),
    verbose: Optional[bool] = typer.Option(
        False, "--verbose", "-v", help="Display standard output from conda"
    ),
):
    """
    Re-create an environment from lock file.
    """
    if file:
        if Path(file).is_file():
            if name is None:  # pragma: no cover
                name = Path(file).stem
            read_lock_file_and_install(file, name, verbose)
        else:
            console.print(f"[bold red]{file} is not a valid file")
            raise typer.Exit()