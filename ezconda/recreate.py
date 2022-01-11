import subprocess
import typer
import json
from typing import Optional
from pathlib import Path

from .console import console


def read_lock_file_and_install(lock_file: Path, env_name: str, verbose: bool) -> None:
    """
    Reads lock file; identifies packages, their version number and build string and groups them by
    channel and attempts installation.

    If errors are encountered during installation, user is informed.
    """

    with console.status(f"[magenta]Reading lock file") as status:

        with open(lock_file, "r") as f:
            complete_spec = json.load(f)

        # only create environment if lock file load is successful
        status.update(f"[magenta]Creating conda environment {env_name}")

        p = subprocess.run(
            ["conda", "create", "-n", env_name, "-y"], capture_output=True, text=True
        )

        # find the channels in the lock file
        channels = list(set([d["channel"] for d in complete_spec]))

        for channel in channels:
            # get package-version-build for packages from a channel
            status.update(f"[magenta]Collecting packages for channel : {channel}")

            pvb = [
                f"{d['name']}={d['version']}={d['build_string']}"
                for d in complete_spec
                if d["channel"] == channel
            ]
            status.update(f"[magenta]Installing packages for channel : {channel}")

            p = subprocess.run(
                [
                    "conda",
                    "install",
                    "-n",
                    env_name,
                    *pvb,
                    "-c",
                    channel,
                    "-y",
                ],
                capture_output=True,
                text=True,
            )

            if verbose:
                console.print(f"[bold yellow]{p.stdout}")

            if p.returncode != 0:
                console.print("[red]" + str(p.stdout + p.stderr))
                raise typer.Exit()

            console.print(
                f"[bold green] :rocket: Installed all packages from channel : {channel}",
            )

        console.print(
            f"[bold green] :star: Installed all dependencies from '{lock_file}'!"
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
