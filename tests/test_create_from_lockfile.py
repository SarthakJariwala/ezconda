import os
import pytest
from typer.testing import CliRunner
from ezconda.main import app
from .helpers import check_if_env_is_created, check_if_pkg_is_installed


runner = CliRunner()


@pytest.mark.usefixtures("clean_up_env_after_test")
def test_create_w_non_existing_file(clean_up_env_after_test):
    result = runner.invoke(
        app, ["create", "-f", "does_not_exist.lock"]
    )
    assert "File provided does not exist" in result.stdout


@pytest.mark.usefixtures("clean_up_env_after_test")
def test_create_from_lockfile_wo_env_name(clean_up_env_after_test):
    _ = runner.invoke(
        app, ["create", "-n", "test", "-c", "conda-forge", "python=3.9", "typer"]
    )

    for file in os.listdir():
        if file.endswith(".lock") and file != "poetry.lock":
            lock_file = file
    result = runner.invoke(app, ["create", "-f", lock_file])

    check_if_env_is_created("test")
    check_if_pkg_is_installed("test", "typer", channel="conda-forge")


@pytest.mark.usefixtures("clean_up_env_after_test")
def test_create_from_lockfile_with_verbose(clean_up_env_after_test):
    _ = runner.invoke(
        app, ["create", "-n", "test", "-c", "conda-forge", "python=3.9", "typer"]
    )

    for file in os.listdir():
        if file.endswith(".lock") and file != "poetry.lock":
            lock_file = file
    result = runner.invoke(app, ["create", "-f", lock_file, "-v"])

    check_if_env_is_created("test")
    check_if_pkg_is_installed("test", "typer", channel="conda-forge")


@pytest.mark.usefixtures("clean_up_env_after_test")
def test_create_from_lockfile_w_env_name(clean_up_env_after_test):
    _ = runner.invoke(
        app, ["create", "-n", "test", "-c", "conda-forge", "python=3.9", "typer"]
    )

    for file in os.listdir():
        if file.endswith(".lock") and file != "poetry.lock":
            lock_file = file
    env_name = "test2"
    result = runner.invoke(app, ["create", "-f", lock_file, "-n", env_name])

    check_if_env_is_created("test2")
    check_if_pkg_is_installed("test2", "typer", channel="conda-forge")
