import json
import re
import subprocess
import yaml
import typer
from pathlib import Path
from typing import Optional, Dict, List
from textwrap import dedent

from .console import console


def create_initial_env_specs(
    env_name: str, channel: Optional[str] = None, packages: Optional[List[str]] = None
) -> Dict:
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


def get_validate_file_name(env_name: str, file: Optional[str] = None) -> Optional[str]:
    """
    Looks for a '.yml' file with the `env_name` specified. If file cannot
    be located, prompt will ask for the file name. If the file provided does
    not exist, the program will exit.
    """

    if not file:
        # first look for existing yml file
        if not Path(f"{env_name}.yml").is_file():
            console.print(f"[yellow]Couldn't locate {env_name}.yml")
            console.print(
                dedent(
                    f"""
            [yellow]If your environment name and specifications file name are not the same,
            please provide the specifications file name to update using the '-f' or '--file' flag.
            """
                )
            )
            raise typer.Exit()
        else:
            file = Path(f"{env_name}.yml")
    # validate the file that the user provides
    else:
        if not Path(file).is_file():
            console.print(f"[magenta]Could not locate '{file}'")
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

    existing_packages = env_specs.get("dependencies")

    # check if packages already exists
    if existing_packages:
        # create a list of existing packages without >,<,=
        existing_packages_re = [re.findall(r"\w+", d)[0] for d in existing_packages]

        for pkg in pkg_name:
            # strip any >,<,= from the package name that the user provided
            pkg_re = re.findall(r"\w+", pkg)[0]

            # exit if package already exists in the env.yml file
            if pkg_re in existing_packages_re:
                console.print(
                    f"[yellow]'{pkg_re}' already exists. Skipping installation.\n"
                    f"[yellow]If you want to update {pkg_re}, use `update` instead."
                )
                raise typer.Exit()

        env_specs["dependencies"] = existing_packages + list(pkg_name)
    else:
        env_specs["dependencies"] = list(pkg_name)
    return env_specs


def add_new_channel_to_env_specs(env_specs: Dict, channel: Optional[str]) -> Dict:
    """Add new channel to the environment specifications, if it does not exist."""

    # this should always return ["defaults"] atleast!
    if channel:
        existing_channels = list(env_specs.get("channels"))
        if existing_channels and channel not in existing_channels:
            existing_channels.append(channel)
            env_specs["channels"] = existing_channels
    return env_specs


def remove_pkg_from_dependencies(env_specs: Dict, pkg_name: List[str]) -> Dict:
    """
    Checks if the package/s specified already exist in 'dependencies' section in 'yml' file.
    If package/s does not exist, informs user and exits the program.
    If package/s exist, remove it from 'dependencies' section in 'yml' file.
    """

    existing_packages = env_specs.get("dependencies")

    # check if packages exists in specifications
    if existing_packages:
        # create a list of existing packages without >,<,=
        existing_packages_re = [re.findall(r"\w+", d)[0] for d in existing_packages]
        for pkg in pkg_name:
            # strip any >,<,= from the package name that the user provided
            pkg_re = re.findall(r"\w+", pkg)[0]

            # check if the package exists in the existing packages list
            if pkg_re not in existing_packages_re:
                console.print(
                    f"[bold red]'{pkg}' is not listed in '{env_specs['name']}.yml' file!"
                )
                raise typer.Exit()

            # this will only run if the package was found in the existing packages list
            for ext_pkg_re, ext_pkg in zip(existing_packages_re, existing_packages):
                if pkg_re == ext_pkg_re:
                    existing_packages.remove(ext_pkg)
                    existing_packages_re.remove(
                        ext_pkg_re
                    )  # need to remove it from this list as well otherwise zip will create an issue
                    env_specs["dependencies"] = existing_packages

    else:
        console.print(
            f"[bold red]There are no packages listed in '{env_specs['name']}.yml' file."
        )
        raise typer.Exit()
    return env_specs


def update_channels_after_removal(env_specs: Dict, env_name: str) -> Dict:
    """
    Updates channels in the environment specifications by looking at the exisiting channels in the environment.
    """

    # get list of channels
    p = subprocess.run(
        ["conda", "list", "-n", env_name, "--json"], capture_output=True, text=True
    )

    # identify unique ones and update channels in env_specs
    complete_dict: List[Dict] = json.loads(p.stdout)
    new_channels = list(set([d["channel"] for d in complete_dict]))
    new_channels.append("defaults")  # 'defaults' needs to be added back?
    env_specs["channels"] = new_channels
    return env_specs


def recheck_dependencies(env_specs: Dict, env_name: str) -> Dict:
    """
    Check if while removing a package, any dependent packages are also removed from env
    but not from .yml file. If so, remove them from .yml file
    """
    p = subprocess.run(
        ["conda", "list", "-n", env_name, "--json"], capture_output=True, text=True
    )
    complete_dict = json.loads(p.stdout)
    all_pkgs = set([d["name"] for d in complete_dict])

    deps = env_specs["dependencies"]  # this may have dependencies with ">,<,=" symbols
    deps_re = [re.findall(r"\w+", d)[0] for d in deps]  # removing the symbols

    rem_pkgs_to_be_removed_from_yml = set(deps_re) - all_pkgs
    if rem_pkgs_to_be_removed_from_yml:
        if "python" in rem_pkgs_to_be_removed_from_yml:
            rem_pkgs_to_be_removed_from_yml.remove("python")
        env_specs = remove_pkg_from_dependencies(
            env_specs, rem_pkgs_to_be_removed_from_yml
        )

    return env_specs
