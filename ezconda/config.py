import typer
from pathlib import Path
from typing import Optional, Dict
import tomlkit

from .solver import Solver

from .console import console


# get ezconda config file
app_dir = typer.get_app_dir("ezconda")
config_file: Path = Path(app_dir) / "config.toml"


def check_configs(
    app_dir: str = app_dir, config_file: Path = config_file
) -> Optional[Dict]:
    """
    Check app config file for user settings.
    Retruns a dict of configs if they exist.
    """

    # check if directory exists
    if Path(app_dir).is_dir():
        # check if config file exists
        if config_file.is_file():
            with open(config_file, "r") as f:
                configs = tomlkit.load(f)
            return configs


def make_and_read_config_file(
    app_dir: str = app_dir, config_file: Path = config_file
) -> Dict:
    """Create config file if it doesn't exist and return empty dict of configs.
    If one exists, read it and return a dict of configs."""

    # create app directory if it doesn't exist
    if not Path(app_dir).is_dir():
        Path(app_dir).mkdir(parents=True)

    # create config file if it doesn't exist
    # this will happen the first time config is run
    if not config_file.is_file():
        config_file.touch()
        configs = {}

    else:
        with open(config_file, "r") as f:
            configs = tomlkit.load(f)

    return configs


def get_default_solver() -> Solver:
    """Checks config file for default solver.
    If config file or solver related config doesn't exist,
    returns mamba as default solver.
    """
    config = check_configs()

    if config:
        if config.get("solver") is not None:
            solver = config["solver"]
        else:
            solver = Solver.mamba
    else:
        solver = Solver.mamba
    return solver


def config(
    solver: Solver = typer.Option(
        None,
        "--solver",
        help="Set default solver",
        case_sensitive=False,
    ),
    show: bool = typer.Option(False, "--show", help="Show current config"),
):
    """
    Configure default settings for ezconda
    """
    configs = make_and_read_config_file()

    if solver:
        configs.update({"solver": solver})

    with open(config_file, "w") as f:
        tomlkit.dump(configs, f)

    if show:
        console.print(f"[bold green]Current Configuration")
        console.print_json(data=configs)
