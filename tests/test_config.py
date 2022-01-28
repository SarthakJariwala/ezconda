from typing import Dict
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
def test_make_config_file(delete_config_file):
    # check that it doesn't exist
    assert not config_file.is_file()

    # create config file
    configs = make_and_read_config_file(app_dir, config_file)

    # check that it exists after creation
    assert config_file.is_file()
    # because it didn't exist before, configs dict should be empty
    assert configs == {}


def test_default_solver_when_none_is_set():
    solver = get_default_solver()
    assert solver == Solver.mamba


@pytest.mark.usefixtures("delete_config_file")
def test_default_solver_after_setting_it(delete_config_file):
    result = runner.invoke(app, ["config", "--solver", "conda"])

    # check if it was successful
    assert result.exit_code == 0

    # check that a config file was created
    assert config_file.is_file()

    # check that the default solver is set to conda
    solver = get_default_solver()
    assert solver == Solver.conda
