import subprocess
import typer
from typing import List, Optional
from pathlib import Path
from conda.cli.python_api import Commands
from conda.cli.python_api import run_command

from .console import console
from ._utils import create_initial_env_specs, write_env_file
from .experimental import write_lock_file


def create(
    name: str = typer.Option(
        ...,
        "--name",
        "-n",
        prompt="Name of the new environment",
        help="Name of the environment to create",
    ),
    packages: List[str] = typer.Argument(None, help="Additional packages to install"),
    channel: Optional[str] = typer.Option(
        None, "--channel", "-c", help="Additional channel to search for packages"
    ),
    file: Optional[Path] = typer.Option(
        None, "--file", "-f", help="Name of the environment yml file"
    ),
    verbose: Optional[bool] = typer.Option(
        False, "--verbose", "-v", help="Display standard output from conda"
    ),
    lock: Optional[bool] = typer.Option(True, help="Generate and write lockfile"),
):
    """
    Create new conda environment with a corresponding environment file and 'lock' file.

    Environment file contains environment specifications and 'lock' file contains complete
    specifications for reproducible environment builds.
    """

    # create a yml file to write specs to
    if file is None:
        file = Path(f"{name}.yml")

    # check if file (and likely environment) already exists
    if file.is_file():
        overwrite = typer.confirm(
            f"""
            There is an existing {file} file.

            Please note that this likely means you have an existing conda environment with the same name as {name}.
            
            Do you want to update the file and environment?
            
            Answering "Yes"/"y" will create a new conda environment '{name}' and overwrite '{file}'.
            """,
            abort=True,
        )
        console.print(f"[bold yellow]Overwrite {file} ...")

    env_specs = create_initial_env_specs(name, channel, packages)

    with console.status(f"[magenta]Creating new conda environment {name}") as status:

        if packages:
            status.update(status="[magenta]Resolving & Installing packages")

        if not channel:
            p = subprocess.run(
                ["conda", "create", "-n", name, *packages, "-y"],
                capture_output=True,
                text=True,
            )

        else:
            p = subprocess.run(
                [
                    "conda",
                    "create",
                    "-n",
                    name,
                    "--channel",
                    channel,
                    *packages,
                    "-y",
                ],
                capture_output=True,
                text=True,
            )

        if p.returncode != 0:
            console.print(f"[red]{str(p.stdout + p.stderr)}")
            raise typer.Exit()

        if verbose:
            console.print(f"[bold yellow]{str(p.stdout)}")

        console.print(f"[bold green] :rocket: Created '{name}' environment")

        status.update(f"[magenta]Writing specifications to {file}")
        write_env_file(env_specs, file)
        console.print(f"[bold green] :floppy_disk: Saved specifications to '{file}'")

        if (
            lock and packages
        ):  # only write lock file if packages are mentioned during env creation
            status.update(
                f"[yellow]:warning: EXPERIMENTAL :warning: [magenta]Writing lock file "
            )

            write_lock_file(name)
            console.print(
                f"[bold green] :lock: Lock file generated [bold yellow]:warning: EXPERIMENTAL :warning:"
            )

        console.print(f"[bold green] :star: Done!")
