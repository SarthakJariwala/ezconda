import subprocess
from textwrap import dedent
import typer
from typing import List, Optional
from pathlib import Path

from ezconda.recreate import read_lock_file_and_install

from .console import console
from ._utils import create_initial_env_specs, write_env_file, read_env_file
from .solver import Solver
from .summary import get_summary_for_revision
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
        None, "--file", "-f", help="Name of the environment specifications (.yml) file or lock file (.lock)"
    ),
    summary: bool = typer.Option(
        True, "--summary", help="Show summary of changes made"
    ),
    verbose: Optional[bool] = typer.Option(
        False, "--verbose", "-v", help="Display standard output from conda"
    ),
    lock: Optional[bool] = typer.Option(True, help="Generate and write lockfile"),
):
    """
    Create new conda environment with a corresponding environment specifications file and lock file.
    Alternatively, also create an environment from existing specifications file or lock file.

    Environment file contains environment specifications and 'lock' file contains complete
    specifications for reproducible environment builds.
    """
    if solver is None:
        solver = get_default_solver()

    # create a yml file to write specs if not creating from existing files
    if file is None:
        if name is None:
            name = typer.prompt("Name of the environment to create")

        file = Path(f"{name}.yml")

        # check if file (and likely environment) already exists
        if file.is_file():
            overwrite = typer.confirm(
                dedent(
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

        with console.status(
            f"[magenta]Creating new conda environment {name}"
        ) as status:

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
            console.print(
                f"[bold green] :floppy_disk: Saved specifications to '{file}'"
            )

            if (
                lock and packages
            ):  # only write lock file if packages are mentioned during env creation
                status.update(f"[magenta]Writing lock file")

                write_lock_file(name)

    elif file.is_file():
        # create from lock file
        if file.suffix == ".lock":
            read_lock_file_and_install(file, solver, verbose, name)
        else:
            # create from yml spec file
            with console.status(
                f"[magenta]Creating new conda environment using {file}"
            ) as status:

                p = subprocess.run(
                    [f"{solver.value}", "env", "create", "--file", file],
                    capture_output=True,
                    text=True,
                )

                if p.returncode != 0:
                    console.print(f"[red]{str(p.stdout + p.stderr)}")
                    raise typer.Exit()

                # get env name from yml file
                name = read_env_file(file)["name"]
                console.print(f"[bold green] :rocket: Created '{name}' environment")

                if (
                    lock
                ):  # only write lock file if packages are mentioned during env creation
                    status.update(f"[magenta]Writing lock file")
                    write_lock_file(name)

                if verbose:
                    console.print(f"[bold yellow]{str(p.stdout)}")

        console.print(f"[bold green] :star: Done!")

    if summary:
        get_summary_for_revision(name)
