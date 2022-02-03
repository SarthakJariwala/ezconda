import subprocess
import tempfile
import typer
from typing import Optional
from pathlib import Path

from .console import console
from .solver import Solver
from .config import get_default_solver
from .files.lockfile import LockFile


def read_lock_file_and_install(
    lock_file: Path,
    solver: Solver,
    verbose: bool,
    env_name: Optional[str] = None,
) -> None:
    """
    Reads lock file, verifies the content and creates a new environment
    with packages specifed in the lock file.
    """

    with console.status(f"[magenta]Reading lock file") as status:

        l = LockFile()
        complete_specs = l.read_lock_file(lock_file)

        l.verify_lock_file_contents(complete_specs)

        if env_name is None:
            env_name = complete_specs["environment"]["name"]

        explicit_specs = [
            f"{pkg['base_url']}/{pkg['platform']}/{pkg['dist_name']}"
            for pkg in complete_specs["packages"]
            if not pkg["channel"].startswith("pypi")
        ]

        explicit_specs = [
            spec + ".conda"
            if spec.startswith("https://repo.anaconda.com")
            else spec + ".tar.bz2"
            for spec in explicit_specs
        ]

        with tempfile.NamedTemporaryFile() as f:
            f.write(bytes("@EXPLICIT\n", "utf-8"))
            f.writelines([bytes(specs + "\n", "utf-8") for specs in explicit_specs])
            f.flush()

            status.update(f"[magenta]Creating new conda environment {env_name}")

            p = subprocess.run(
                [
                    f"{solver.value}",
                    "create",
                    "-n",
                    env_name,
                    "--file",
                    f"{f.name}",
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

        # TODO: Add installation for pypi channels/packages

        console.print(
            f"[bold green] :rocket: Recreated '{env_name}' environment from lock file",
        )


def recreate(
    file: Path = typer.Argument(
        ..., help="Lock file to use to re-create an environment"
    ),
    name: Optional[str] = typer.Option(
        None,
        "--name",
        "-n",
        help="Name of the environment to create",
    ),
    solver: Solver = typer.Option(None, help="Solver to use", case_sensitive=False),
    verbose: Optional[bool] = typer.Option(
        False, "--verbose", "-v", help="Display standard output from conda"
    ),
):
    """
    Re-create an environment from lock file. This will install all the packages
    specified in the lock file, if the system and platform match lock file.
    """

    if solver is None:
        solver = get_default_solver()

    read_lock_file_and_install(file, solver, verbose, name)
