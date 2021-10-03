import json
import subprocess
from typing import List, Optional
from pathlib import Path
import time
import typer
import os
import conda.exports
from conda.cli.python_api import run_command
from conda.cli.python_api import Commands
from rich.prompt import Confirm

from . import __version__
from ._utils import (
    create_initial_env_specs,
    get_validate_file_name,
    read_env_file,
    add_pkg_to_dependencies,
    write_env_file,
    add_new_channel_to_env_specs,
    remove_pkg_from_dependencies,
    update_channels_after_removal,
)
from .console import console
from .experimental import write_lock_file, read_lock_file_and_install


app = typer.Typer()


@app.command()
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
    lock: Optional[bool] = typer.Option(True, help="Write lockfile"),
    from_lock: Optional[str] = typer.Option(
        None, "--from-lock", help="Create environment from lock file"
    ),
):
    """
    Create new conda environment with a corresponding environment file and 'lock' file.

    Environment file contains environment specifications and 'lock' file contains complete
    specifications for reproducible environment builds.
    """
    if from_lock:
        if Path(from_lock).is_file():
            read_lock_file_and_install(from_lock, name, verbose)
        else:
            console.print(f"[bold red]{from_lock} is not a valid file")
            raise typer.Exit()
    else:
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

        with console.status(
            f"[magenta]Creating new conda environment {name}"
        ) as status:
            time.sleep(1)

            if packages:
                status.update(status="[magenta]Resolving packages")
                time.sleep(1)

            if not channel:
                stdout, stderr, exit_code = run_command(
                    Commands.CREATE, "-n", name, *packages, use_exception_handler=True
                )

            else:
                stdout, stderr, exit_code = run_command(
                    Commands.CREATE,
                    "-n",
                    name,
                    "--channel",
                    channel,
                    *packages,
                    use_exception_handler=True,
                )

            if exit_code != 0:
                console.print(f"[red]{str(stdout + stderr)}")
                raise typer.Exit()

            if verbose:
                console.print(f"[bold]{stdout}")

            console.print(f"[bold green] :rocket: Created '{name}' environment")

            status.update(f"[magenta]Writing specifications to {file}")
            time.sleep(1)
            write_env_file(env_specs, file)
            console.print(
                f"[bold green] :floppy_disk: Written specifications to '{file}'"
            )

            if (
                lock and packages
            ):  # only write lock file if packages are mentioned during env creation
                status.update(
                    f"[yellow]:warning: EXPERIMENTAL :warning: [magenta]Writing lock file "
                )
                time.sleep(1)
                write_lock_file(name)
                console.print(
                    f"[bold green] :lock: Lock file generated [bold yellow]:warning: EXPERIMENTAL :warning:"
                )

            console.print(f"[bold green] :star: Done!")


@app.command()
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
        time.sleep(1)
        file = get_validate_file_name(env_name, file)

        env_specs = read_env_file(file)
        env_specs = add_pkg_to_dependencies(env_specs, pkg_name)
        env_specs = add_new_channel_to_env_specs(env_specs, channel)

        status.update("[magenta]Installing packages")
        time.sleep(1)

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
        time.sleep(1)
        write_env_file(env_specs, file)
        console.print(f"[bold green] :floppy_disk: Written specifications to '{file}'")

        if lock:
            status.update(
                f"[yellow]:warning: EXPERIMENTAL :warning: [magenta]Writing lock file "
            )
            time.sleep(1)
            write_lock_file(env_name)
            console.print(
                f"[bold green] :lock: Lock file generated [bold yellow]:warning: EXPERIMENTAL :warning:"
            )

        console.print(f"[bold green] :star: Done!")


@app.command()
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
        linked_data = conda.exports.linked_data(os.path.expanduser("~/anaconda"))

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
        time.sleep(1)

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
        time.sleep(1)
        write_env_file(env_specs, file)
        console.print(f"[bold green] :floppy_disk: Written specifications to '{file}'")

        if lock:
            status.update(
                f"[yellow]:warning: EXPERIMENTAL :warning: [magenta]Writing lock file "
            )
            time.sleep(1)
            write_lock_file(env_name)
            console.print(
                f"[bold green] :lock: Lock file generated [bold yellow]:warning: EXPERIMENTAL :warning:"
            )

        console.print(f"[bold green] :star: Done!")


@app.command()
def version():
    """Shows the version of 'ezconda' installed"""
    console.print(f"[magenta]{__version__}")


# if __name__ == "__main__":
#     app()
