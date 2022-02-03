import typer
from ..console import console
from ..files.lockfile import LockFile


__all__ = ["write_lock_file", "lock"]


def write_lock_file(env_name: str) -> None:
    """
    Writes a lock file for the environment specified.
    """

    lockfile = LockFile()
    lockfile.write_lockfile(env_name)


def lock(
    env_name: str = typer.Option(
        ...,
        "--name",
        "-n",
        prompt="Name of the environment",
        help="Name of the environment to generate lock file for",
    ),
) -> None:
    """
    Generate lock file for a conda environment
    """
    with console.status(f"[magenta]Writing lock file"):
        write_lock_file(env_name)

    console.print(f"[bold green] :star: Done!")
