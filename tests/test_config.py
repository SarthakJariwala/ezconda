import typer
import pytest
from pathlib import Path
from typer.testing import CliRunner

from ezconda.solver import Solver
from ezconda.config import make_and_read_config_file, get_default_solver
from ezconda.main import app


runner = CliRunner()

app_dir = typer.get_app_dir("ezconda")
config_file: Path = Path(app_dir) / "config.json"


@pytest.mark.usefixtures("delete_config_file")
def test_make_config_file(delete_config_file) -> None:
    # check that it doesn't exist
    assert not config_file.is_file()

    # create config file
    configs = make_and_read_config_file(app_dir, config_file)

    # check that it exists after creation
    assert config_file.is_file()
    # because it didn't exist before, configs dict should be empty
    assert configs == {}


@pytest.mark.usefixtures("delete_config_file")
def test_make_and_read_config_file(delete_config_file) -> None:
    # create config file with the config command
    result = runner.invoke(app, ["config", "--solver", "conda"])

    # check that we can read the config file after creation
    configs = make_and_read_config_file(app_dir, config_file)
    # check what we set was saved in the configs file
    assert configs["solver"] == "conda"


def test_default_solver_when_none_is_set() -> None:
    solver = get_default_solver()
    assert solver == Solver.mamba


@pytest.mark.usefixtures("delete_config_file")
def test_default_solver_after_setting_it(delete_config_file) -> None:
    result = runner.invoke(app, ["config", "--solver", "conda"])

    # check if it was successful
    assert result.exit_code == 0

    # check that a config file was created
    assert config_file.is_file()

    # check that the default solver is set to conda
    solver = get_default_solver()
    assert solver == Solver.conda


@pytest.mark.usefixtures("delete_config_file")
def test_show_configs(delete_config_file) -> None:
    _ = runner.invoke(app, ["config", "--solver", "conda"])

    result = runner.invoke(app, ["config", "--show"])

    assert 'Current Configuration\n{\n  "solver": "conda"\n}\n' in result.stdout
