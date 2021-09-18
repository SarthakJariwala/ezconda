from conda.cli.python_api import Commands, run_command
import typer
import json
import subprocess
from subprocess import PIPE

__all__ = ["write_lock_file"]


def write_lock_file(env_name):
    typer.secho(f"Writing lockfile...", fg=typer.colors.YELLOW)
    # generate lockfile
    # o = subprocess.run(["conda", "list", "-n", f"{env_name}", "--json"], stdout=PIPE)
    stdout, stderr, exit_code = run_command(Commands.LIST, "-n", f"{env_name}", "--json")
    with open(f"{env_name}.lockfile", "w") as f:
        json.dump(json.loads(stdout), f, indent=4)
    typer.secho(f"Done!", fg=typer.colors.BRIGHT_GREEN)