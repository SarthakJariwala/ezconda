import pytest
from typer.testing import CliRunner
from ezconda.main import app
from ezconda._utils import read_env_file, add_pkg_to_dependencies, write_env_file
from .test_install import check_if_pkg_is_installed


runner = CliRunner()


@pytest.mark.usefixtures("clean_up_env_after_test")
def test_env_sync_w_spec_file():
    # create a new environment
    _ = runner.invoke(app, ["create", "-n", "test", "python=3.9"])

    # add package to the spec file
    env_specs = read_env_file("test.yml")
    env_specs = add_pkg_to_dependencies(env_specs, ["numpy"])
    write_env_file(env_specs, "test.yml")

    # sync the environment
    result = runner.invoke(app, ["sync", "-n", "test"])

    assert result.exit_code == 0

    # check if numpy is in the environment
    check_if_pkg_is_installed("test", "numpy")


@pytest.mark.usefixtures("clean_up_env_after_test")
def test_verbose_install_w_conda(clean_up_env_after_test):
    _ = runner.invoke(app, ["create", "-n", "test", "python=3.9"])

    # add package to the spec file
    env_specs = read_env_file("test.yml")
    env_specs = add_pkg_to_dependencies(env_specs, ["numpy"])
    write_env_file(env_specs, "test.yml")

    result = runner.invoke(
        app, ["sync", "-n", "test", "-v", "--solver", "conda"]
    )

    assert result.exit_code == 0

    check_if_pkg_is_installed("test", "numpy")