from conda.cli.python_api import Commands, run_command
from pathlib import Path
import typer
import json

__all__ = ["write_lock_file", "read_lock_file_and_install"]


def write_lock_file(env_name) -> None:
    """
    Writes a lock file for the environment specified.
    """
    typer.secho(f"Writing lock file... [EXPERIMENTAL]", fg=typer.colors.YELLOW)
    # generate lock file
    stdout, _, _ = run_command(Commands.LIST, "-n", f"{env_name}", "--json")
    complete_specs = json.loads(stdout)
    # get the platform from specs listed
    platform = list(set([d["platform"] for d in complete_specs]))
    if "noarch" in platform:
        platform.remove("noarch")

    # write lock file
    with open(f"{env_name}-{platform[0]}.lock", "w") as f:
        json.dump(complete_specs, f, indent=4)
    typer.secho(f"Done!", fg=typer.colors.BRIGHT_GREEN)


def read_lock_file_and_install(lock_file: Path, env_name: str, verbose: bool) -> None:
    """
    Reads lock file; identifies packages, their version number and build string and groups them by
    channel and attempts installation.

    If errors are encountered during installation, user is informed.
    """

    typer.secho(f"Creating environment {env_name}...", fg=typer.colors.YELLOW)
    _ = run_command(Commands.CREATE, "-n", env_name, use_exception_handler=True)
    typer.secho(f"Reading lock file... [EXPERIMENTAL]", fg=typer.colors.YELLOW)
    with open(lock_file, "r") as f:
        complete_spec = json.load(f)

    channels = list(set([d["channel"] for d in complete_spec]))

    for channel in channels:
        # get package-version-build for packages from a channel
        typer.secho(
            f"Collecting packages for channel : {channel}", fg=typer.colors.YELLOW
        )
        pvb = [
            f"{d['name']}={d['version']}={d['build_string']}"
            for d in complete_spec
            if d["channel"] == channel
        ]
        typer.secho(
            f"Installing packages for channel : {channel}", fg=typer.colors.YELLOW
        )
        stdout, stderr, exit_code = run_command(
            Commands.INSTALL, "-n", env_name, *pvb, "-c", channel
        )

        if verbose:
            typer.echo(stdout)

        if exit_code != 0:
            typer.secho(str(stdout + stderr), color=typer.colors.BRIGHT_RED)
            raise typer.Exit()
        typer.secho(
            f"Installed all packages from channel : {channel}",
            fg=typer.colors.BRIGHT_GREEN,
        )

    typer.secho(
        f"Installed all dependencies from '{lock_file}'!", fg=typer.colors.BRIGHT_GREEN
    )
