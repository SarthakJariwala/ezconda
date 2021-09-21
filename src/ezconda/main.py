from typing import List, Optional
from pathlib import Path
import typer
from conda.cli.python_api import run_command
from conda.cli.python_api import Commands

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
from .experimental import write_lock_file, read_lock_file_and_install


app = typer.Typer()


@app.command()
def create(
    name: str = typer.Option(
        ..., "--name", "-n", help="Name of the environment to create"
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
            typer.secho(f"{from_lock} is not a valid file!", fg=typer.colors.BRIGHT_RED)
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
            typer.secho(f"Overwriting {file} ...", fg=typer.colors.YELLOW)

        env_specs = create_initial_env_specs(name, channel, packages)

        typer.secho(
            f"Creating new conda environment : {name} ...", fg=typer.colors.YELLOW
        )

        if packages:
            typer.secho(f"Resolving packages...\n", fg=typer.colors.YELLOW)

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
            typer.secho(str(stdout + stderr), color=typer.colors.BRIGHT_RED)
            raise typer.Exit()

        if verbose:
            typer.echo(stdout)

        typer.secho(
            f"""Done! You can activate it with :         
        
        $ conda activate {name}
            """,
            fg=typer.colors.GREEN,
        )

        typer.secho(f"Writing specifications to {file} ...", fg=typer.colors.GREEN)
        write_env_file(env_specs, file)

        typer.secho(f"Created {file}!", fg=typer.colors.GREEN)

        if lock:
            write_lock_file(name)


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

    typer.secho("Validating file, packages, channels...", fg=typer.colors.YELLOW)
    file = get_validate_file_name(env_name, file)

    env_specs = read_env_file(file)
    env_specs = add_pkg_to_dependencies(env_specs, pkg_name)
    env_specs = add_new_channel_to_env_specs(env_specs, channel)

    typer.secho("Installing packages...", fg=typer.colors.YELLOW)

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
        typer.secho(str(stdout + stderr), color=typer.colors.BRIGHT_RED)
        raise typer.Exit()

    if verbose:
        typer.echo(stdout)

    typer.secho("Installation complete!\n", fg=typer.colors.GREEN)

    typer.secho(f"Updating {file}...", fg=typer.colors.YELLOW)
    write_env_file(env_specs, file)
    typer.secho(f"Updated {file}!\n", fg=typer.colors.GREEN)

    if lock:
        write_lock_file(env_name)


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

    typer.secho("Validating file, packages...", fg=typer.colors.YELLOW)
    file = get_validate_file_name(env_name, file)

    env_specs = read_env_file(file)
    env_specs = remove_pkg_from_dependencies(env_specs, pkg_name)

    typer.secho("Removing packages...", fg=typer.colors.YELLOW)

    stdout, stderr, exit_code = run_command(
        Commands.REMOVE, "-n", env_name, *pkg_name, use_exception_handler=True
    )

    if exit_code != 0:
        typer.secho(str(stdout + stderr), color=typer.colors.BRIGHT_RED)
        raise typer.Exit()

    if verbose:
        typer.echo(stdout)

    env_specs = update_channels_after_removal(env_specs, env_name)

    typer.secho("Removal complete!\n", fg=typer.colors.GREEN)

    typer.secho(f"Updating {file}...", fg=typer.colors.YELLOW)
    write_env_file(env_specs, file)
    typer.secho(f"Updated {file}!\n", fg=typer.colors.GREEN)

    if lock:
        write_lock_file(env_name)


if __name__ == "__main__":
    app()
