from conda.cli.python_api import Commands, run_command
from pathlib import Path
import typer
import json
from ..console import console


__all__ = ["write_lock_file"]


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
