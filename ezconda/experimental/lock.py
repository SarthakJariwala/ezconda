from conda.cli.python_api import Commands, run_command
from pathlib import Path
import typer
import json
from ..console import console


__all__ = ["write_lock_file", "lock"]


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


def lock(
    env_name: str = typer.Option(
        ...,
        "--name",
        "-n",
        prompt="Name of the environment",
        help="Name of the environment to generate lock file for",
    ),
):
    """
    Generate lock file for a conda environment
    """
    with console.status(
        f"[yellow]:warning: EXPERIMENTAL :warning: [magenta]Writing lock file"
    ):
        write_lock_file(env_name)
        console.print(
            f"[bold green] :lock: Lock file generated for {env_name} [bold yellow]:warning: EXPERIMENTAL :warning:"
        )
    console.print(f"[bold green] :star: Done!")
