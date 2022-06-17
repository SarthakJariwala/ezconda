import pytest
from typer.testing import CliRunner
from ezconda.main import app
from ezconda._utils import read_env_file, write_env_file


runner = CliRunner()


@pytest.mark.usefixtures("clean_up_env_after_test")
def test_env_sync_w_lockfile():
    # create a new environment with packages
    _ = runner.invoke(app, ["create", "-n", "test", "python=3.8", "numpy<1.20"])

    # remove "<" dependencies from numpy
    env_specs = read_env_file("test.yml")
    env_specs["dependencies"][-1] = "numpy"
    write_env_file(env_specs, "test.yml")

    # update the environment test2 with new test2 lockfile
    result = runner.invoke(app, ["update", "-n", "test"])

    assert result.exit_code == 0
