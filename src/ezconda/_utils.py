import yaml
import typer
from pathlib import Path
from typing import Optional, Dict, List


def create_initial_env_specs(
    env_name : str,
    channel : Optional[str] = None,
    packages : Optional[List[str]] = None
):
    """Create initial environment specifications that will be written to 'yml' file."""

    env_specs = {}
    env_specs.update({"name": env_name})
    if channel:
        env_specs.update({"channels": [channel, "defaults"]})
    else:
        env_specs.update({"channels": ["defaults"]})
    if packages:
        env_specs.update({"dependencies": packages})
    return env_specs


def get_validate_file_name(env_name : str, file: Optional[str] = None) -> Optional[str]:
    """
    Looks for a '.yml' file with the `env_name` specified. If file cannot
    be located, prompt will ask for the file name. If the file provided does
    not exist, the program will exit.
    """

    if not file:
        # first look for existing yml file
        if not Path(f"{env_name}-env.yml").is_file():
            typer.secho(f"Couldn't locate {env_name}-env.yml", fg=typer.colors.YELLOW)
            env_file = typer.prompt("Please provide the environment file to update")
            # check if new file provided is valid
            if Path(env_file).is_file():
                file = Path(env_file)
            else:
                typer.secho(f"Could not locate {env_file}'", fg=typer.colors.BRIGHT_RED)
                raise typer.Exit()
        else:
            file = Path(f"{env_name}-env.yml")
    # validate the file that the user provides
    else:
        if not Path(file).is_file():
            typer.secho(f"Could not locate {file}'", fg=typer.colors.BRIGHT_RED)
            raise typer.Exit()
    return file


def read_env_file(file: str) -> Dict:
    "Read '.yml' file and return a dict containing specifications in the file."

    with open(file, "r") as f:
        env_specs = yaml.load(f, Loader=yaml.FullLoader)
        return env_specs


def write_env_file(env_specs: Dict, file: str) -> None:
    "Writes '.yml' file based on the specifications provided."

    with open(file, "w") as f:
        yaml.safe_dump(env_specs, f, sort_keys=False)


def add_pkg_to_dependencies(env_specs: Dict, pkg_name: List[str]) -> Dict:
    """
    Checks if the package/s specified already exist in 'dependencies' section in 'yml' file.
    If package/s already exists, informs user and exits the program.
    If package/s does not exist, adds it to 'dependencies' section in 'yml' file.
    """

    # TODO - check how this handles multiple '>'/'<' dependencies
    # FOR EXAMPLE - 'numpy>1.1' and 'numpy>1.8' should not lead to two entries in the env.yml file
    existing_packages = env_specs.get("dependencies")
    # check if packages already exists
    if existing_packages:
        for pkg in pkg_name:
            for ext_pkg in existing_packages:
                if pkg in ext_pkg:
                    typer.secho(
                        f"{pkg} already exists. Skipping installation. If you want to update {pkg}, use `update` instead.",
                        fg=typer.colors.YELLOW,
                    )
                    raise typer.Exit()

        env_specs["dependencies"] = existing_packages + list(pkg_name)
    else:
        env_specs["dependencies"] = list(pkg_name)
    return env_specs


def add_new_channel_to_env_specs(env_specs : Dict, channel : Optional[str]) -> Dict:
    """Add new channel to the environment specifications, if it does not exist."""
    if channel:
        existing_channels = list(env_specs.get("channels")) # this should always return ["defaults"] atleast!
        if existing_channels and channel not in existing_channels:
            existing_channels.append(channel)
            env_specs["channels"] = existing_channels
    return env_specs


def remove_pkg_from_dependencies(env_specs: Dict, pkg_name: List[str]) -> Dict:
    """
    Checks if the package/s specified already exist in 'dependencies' section in 'yml' file.
    If package/s already exists, informs user and exits the program.
    If package/s does not exist, adds it to 'dependencies' section in 'yml' file.
    """

    # TODO - check how this handles multiple '>'/'<' dependencies
    # FOR EXAMPLE - 'numpy>1.1' and 'numpy>1.8' should not lead to two entries in the env.yml file
    existing_packages = env_specs.get("dependencies")
    # check if packages already exists
    if existing_packages:
        for pkg in pkg_name:
            if pkg in existing_packages:
                existing_packages.remove(pkg)
                env_specs["dependencies"] = existing_packages
            else:
                typer.secho(
                    f"{pkg} is not listed in environment 'yml' file!",
                    fg=typer.colors.BRIGHT_RED,
                )
                raise typer.Exit()
    else:
        typer.secho("There are no packages listed in the yml file.", fg=typer.colors.BRIGHT_RED)
        raise typer.Exit()
    return env_specs