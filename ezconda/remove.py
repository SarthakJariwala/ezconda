import subprocess
import typer
import time
import json
import os
import conda.exports

from typing import List, Optional

from .console import console
from ._utils import (
    get_validate_file_name,
    read_env_file,
    remove_pkg_from_dependencies,
    write_env_file,
    update_channels_after_removal,
    recheck_dependencies,
)
from .experimental import write_lock_file


def remove(
    pkg_name: List[str] = typer.Argument(..., help="Packages to uninstall"),
    env_name: str = typer.Option(
        ...,
        "--name",
        "-n",
        prompt="Name of the environment to remove from",
        help="Name of the environment to uninstall package from",
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
                f"[magenta]Removing {pkg_name} will also remove the following:"
            )
            console.print(f"[magenta]{other_pkg_that_depends_on_pkg}\n")
            status.stop()
            typer.confirm(f"Do you want to continue?", abort=True)
            status.start()

        env_specs = read_env_file(file)
        env_specs = remove_pkg_from_dependencies(env_specs, pkg_name)

        status.update("[magenta]Removing packages")

        p = subprocess.run(
            [
                "conda",
                "remove",
                "-n",
                env_name,
                *pkg_name,
                "-y",
            ],
            capture_output=True,
            text=True,
        )

        if p.returncode != 0:
            console.print(f"[red]{str(p.stdout + p.stderr)}")
            raise typer.Exit()

        if verbose:
            console.print(f"[yellow]{str(p.stdout)}")

        env_specs = update_channels_after_removal(env_specs, env_name)

        # check if any dependent packages are removed from env but not from .yml file
        # if so, remove them from .yml file
        env_specs = recheck_dependencies(env_specs, env_name)

        console.print(f"[bold green] :rocket: Removed packages from {env_name}")

        status.update(f"[magenta]Writing specifications to {file}")
        write_env_file(env_specs, file)
        console.print(f"[bold green] :floppy_disk: Updated specifications in '{file}'")

        if lock:
            status.update(
                f"[yellow]:warning: EXPERIMENTAL :warning: [magenta]Writing lock file "
            )

            write_lock_file(env_name)
            console.print(
                f"[bold green] :lock: Lock file updated [bold yellow]:warning: EXPERIMENTAL :warning:"
            )

        console.print(f"[bold green] :star: Done!")
