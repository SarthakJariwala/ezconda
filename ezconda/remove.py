import typer
import json
import os
import conda.exports

from typing import List, Optional

from rich.tree import Tree

from .console import console
from ._utils import (
    get_validate_file_name,
    read_env_file,
    remove_pkg_from_dependencies,
    write_env_file,
    update_channels_after_removal,
    recheck_dependencies,
    run_command,
)
from .solver import Solver
from .config import get_default_solver
from .summary import get_summary_for_revision
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
    solver: Solver = typer.Option(None, help="Solver to use", case_sensitive=False),
    file: Optional[str] = typer.Option(
        None, "--file", "-f", help="'.yml' file to update with removed packages"
    ),
    summary: bool = typer.Option(
        True, "--summary", help="Show summary of changes made"
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
        env_specs = read_env_file(file)
        channels = env_specs["channels"]

        installed_packages = [
            specs["name"]
            for specs in json.load(os.popen(f"conda list -n {env_name} --json"))
        ]
        
        for pkg in pkg_name:
            cmd = ["mamba", "repoquery", "whoneeds"]
            for chn in channels:
                cmd.append("-c")
                cmd.append(chn)
            cmd.append(f"{pkg}")
            cmd.append("--json")

            output = run_command(cmd, verbose=False)
            formatted_output = json.loads(output.stdout)
            dependent_pkgs_info = formatted_output["result"]["pkgs"]

            if dependent_pkgs_info:
                dependent_pkgs = [p['name'] for p in dependent_pkgs_info]
                # check if any of the installed packages require this as dep
                intersection_pkgs = set(dependent_pkgs).intersection(set(installed_packages))
                
                if intersection_pkgs:
                    tree = Tree(f"[bold yellow]{pkg} is required by[/]")
                    console.print(f"[bold magenta] :warning: There are packages that depend on {pkg}\n")
                    console.print(f"[bold magenta] :warning: Removing {pkg} will also remove them!\n")
                    for dep_pk in intersection_pkgs:
                        tree.add(f"[bold yellow]{dep_pk}[/]")
                    console.print(tree)
                    status.stop()
                    typer.confirm(f"Do you want to continue?", abort=True)
                    status.start()

        env_specs = read_env_file(file)
        env_specs = remove_pkg_from_dependencies(env_specs, pkg_name)

        status.update("[magenta]Removing packages")

        if solver is None:
            solver = get_default_solver()

        cmd = [
            f"{solver.value}",
            "remove",
            "-n",
            env_name,
            *pkg_name,
            "-y",
        ]

        run_command(cmd, verbose=verbose)

        env_specs = update_channels_after_removal(env_specs, env_name)

        # check if any dependent packages are removed from env but not from .yml file
        # if so, remove them from .yml file
        env_specs = recheck_dependencies(env_specs, env_name)

        console.print(f"[bold green] :cross_mark_button: Removed packages from {env_name}")

        status.update(f"[magenta]Writing specifications to {file}")
        write_env_file(env_specs, file)
        console.print(f"[bold green] :floppy_disk: Updated specifications in '{file}'")

        if lock:
            status.update(f"[magenta]Writing lock file")

            write_lock_file(env_name)

        console.print(f"[bold green] :star: Done!")

        if summary:
            get_summary_for_revision(env_name)
