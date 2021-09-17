from subprocess import run
import typer
import json
import subprocess
from subprocess import PIPE

__all__ = ["write_lock_file"]


def write_lock_file(env_name):
    typer.secho(f"Writing lockfile...", fg=typer.colors.YELLOW)
    # generate lockfile
    o = subprocess.run(["conda", "list", "-n", f"{env_name}", "--json"], stdout=PIPE)
    with open(f"{env_name}.lockfile", "w") as f:
        json.dump(json.loads(o.stdout), f, indent=4)
    typer.secho(f"Done!", fg=typer.colors.BRIGHT_GREEN)