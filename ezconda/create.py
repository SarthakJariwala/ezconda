import subprocess
from textwrap import dedent
import typer
from typing import List, Optional
from pathlib import Path

from .console import console
from ._utils import create_initial_env_specs, write_env_file, read_env_file
from .solver import Solver
from .experimental import write_lock_file
from .config import get_default_solver


def create(
    name: str = typer.Option(
        None,
        "--name",
        "-n",
        help="Name of the environment to create",
    ),
    packages: List[str] = typer.Argument(None, help="Additional packages to install"),
    channel: Optional[str] = typer.Option(
        None, "--channel", "-c", help="Additional channel to search for packages"
    ),
    solver: Solver = typer.Option(None, help="Solver to use", case_sensitive=False),
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
        if name is None:
            name = typer.prompt("Name of the environment to create")
        
        file = Path(f"{name}.yml")

        # check if file (and likely environment) already exists
        if file.is_file():
            overwrite = typer.confirm(dedent(
                f"""
                There is an existing {file} file.

                Please note that this likely means you have an existing conda environment with the same name as {name}.
                
                Do you want to update the file and environment?
                
                Answering "Yes"/"y" will create a new conda environment '{name}' and overwrite '{file}'.
                """,
                ),
                abort=True,
            )
            console.print(f"[bold yellow]Overwrote {file} ...")

        env_specs = create_initial_env_specs(name, channel, packages)

        if solver is None:
            solver = get_default_solver()

        with console.status(f"[magenta]Creating new conda environment {name}") as status:

            if packages:
                status.update(
                    status=f"[magenta]Resolving & Installing packages using {solver.value}"
                )

            if not channel:
                p = subprocess.run(
                    [f"{solver.value}", "create", "-n", name, *packages, "-y"],
                    capture_output=True,
                    text=True,
                )

            else:
                p = subprocess.run(
                    [
                        f"{solver.value}",
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
                status.update(f"[magenta]Writing lock file")

                write_lock_file(name)
        
    elif file.is_file():
        with console.status(f"[magenta]Creating new conda environment using {file}") as status:

            p = subprocess.run(
                ["conda", "env", "create", "--file", file],
                capture_output=True,
                text=True,
            )
            
            if p.returncode != 0:
                console.print(f"[red]{str(p.stdout + p.stderr)}")
                raise typer.Exit()
            
            # get env name from yml file
            env_name = read_env_file(file)["name"]
            console.print(f"[bold green] :rocket: Created '{env_name}' environment")

            if lock:  # only write lock file if packages are mentioned during env creation
                status.update(f"[magenta]Writing lock file")
                write_lock_file(env_name)

            if verbose:
                console.print(f"[bold yellow]{str(p.stdout)}")

    console.print(f"[bold green] :star: Done!")
