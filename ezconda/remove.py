import typer
import time
import json
import os
import conda.exports

from typing import List, Optional
from pathlib import Path
from conda.cli.python_api import Commands
from conda.cli.python_api import run_command

from .console import console
from ._utils import (
    get_validate_file_name,
    read_env_file,
    remove_pkg_from_dependencies,
    write_env_file,
    update_channels_after_removal,
)
from .experimental import write_lock_file


def remove(
    pkg_name: List[str] = typer.Argument(..., help="Packages to uninstall"),
    env_name: str = typer.Option(
        ..., "--name", "-n", help="Name of the environment to uninstall package from"
    ),
    file: Optional[str] = typer.Option(
        None, "--file", "-f", help="'.yml' file to update with removed packages"
    ),
    verbose: Optional[bool] = typer.Option(
        False, "--verbose", "-v", help="Display standard output from conda"
    ),
    lock: Optional[bool] = typer.Option(True, help="Write lockfile"),
):
    """
    Remove/uninstall packages from environment.

    This command will also update the environment file and lockfile.
    """

    with console.status(f"[magenta]Validating file, packages, channels") as status:
        file = get_validate_file_name(env_name, file)

        installed_packages = [
            specs["name"]
            for specs in json.load(os.popen(f"conda list -n {env_name} --json"))
        ]
        root_prefix = json.load(os.popen(f"conda info -e --json"))["root_prefix"]
        linked_data = conda.exports.linked_data(root_prefix)

        other_pkg_that_depends_on_pkg = []
        for k in linked_data.keys():
            if linked_data[k]["name"] in installed_packages:
                # check the dependencies
                # if the package listed for removal is listed as dependency for any other installed package
                # let the user know before they confirm to the removal
                for deps in linked_data[k]["depends"]:
                    for pkg in pkg_name:  # unpack multiple packages
                        if pkg in deps.split(" "):
                            other_pkg_that_depends_on_pkg.append(linked_data[k]["name"])

        if other_pkg_that_depends_on_pkg:
            console.print(f"[magenta]There are packages that depend on {pkg_name}")
            console.print(
                f"[magenta]Removing {pkg_name} will also remove the following:."
            )
            console.print(f"[magenta]{other_pkg_that_depends_on_pkg}\n")
            status.stop()
            typer.confirm(f"Do you want to continue?", abort=True)
            status.start()

        env_specs = read_env_file(file)
        env_specs = remove_pkg_from_dependencies(env_specs, pkg_name)

        status.update("[magenta]Removing packages")
        time.sleep(0.5)

        stdout, stderr, exit_code = run_command(
            Commands.REMOVE, "-n", env_name, *pkg_name, use_exception_handler=True
        )

        if exit_code != 0:
            console.print(f"[red]{str(stdout + stderr)}")
            raise typer.Exit()

        if verbose:
            console.print(f"[yellow]{str(stdout)}")

        env_specs = update_channels_after_removal(env_specs, env_name)

        console.print(f"[bold green] :rocket: Removed packages from {env_name}")

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
