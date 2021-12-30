from conda.cli.python_api import Commands, run_command
from pathlib import Path
import typer
import json
from ..console import console


__all__ = ["write_lock_file", "read_lock_file_and_install"]


def write_lock_file(env_name) -> None:
    """
    Writes a lock file for the environment specified.
    """

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


def read_lock_file_and_install(lock_file: Path, env_name: str, verbose: bool) -> None:
    """
    Reads lock file; identifies packages, their version number and build string and groups them by
    channel and attempts installation.

    If errors are encountered during installation, user is informed.
    """

    console.print(f"[yellow]Creating environment {env_name}")
    _ = run_command(Commands.CREATE, "-n", env_name, use_exception_handler=True)
    console.print(f"[magenta]Reading lock file [EXPERIMENTAL]")
    with open(lock_file, "r") as f:
        complete_spec = json.load(f)

    channels = list(set([d["channel"] for d in complete_spec]))

    for channel in channels:
        # get package-version-build for packages from a channel
        console.print(f"[yellow]Collecting packages for channel : {channel}")
        pvb = [
            f"{d['name']}={d['version']}={d['build_string']}"
            for d in complete_spec
            if d["channel"] == channel
        ]
        console.print(f"[yellow]Installing packages for channel : {channel}")
        stdout, stderr, exit_code = run_command(
            Commands.INSTALL, "-n", env_name, *pvb, "-c", channel
        )

        if verbose:
            typer.echo(stdout)

        if exit_code != 0:
            console.print("[red]" + str(stdout + stderr))
            raise typer.Exit()
        console.print(
            f"[bold green]Installed all packages from channel : {channel}",
        )

    console.print(f"[bold green]Installed all dependencies from '{lock_file}'!")
