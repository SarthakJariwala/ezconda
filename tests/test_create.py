import os
import pytest
from typer.testing import CliRunner
from pathlib import Path
from ezconda.main import app
from .helpers import (
    check_if_channel_is_listed_in_specfile,
    check_if_env_is_created,
    check_if_pkg_is_installed,
    check_if_pkgs_are_listed_in_specfile,
)


runner = CliRunner()


@pytest.mark.usefixtures("clean_up_env_after_test")
def test_create_without_install(clean_up_env_after_test):
    result = runner.invoke(app, ["create", "-n", "test"])

    assert Path("test.yml").is_file()
    check_if_env_is_created("test")


@pytest.mark.usefixtures("clean_up_env_after_test")
def test_create_without_env_name(clean_up_env_after_test):
    result = runner.invoke(app, ["create"], input="test")

    assert Path("test.yml").is_file()
    check_if_env_is_created("test")


@pytest.mark.usefixtures("clean_up_env_after_test")
def test_verbose_w_conda(clean_up_env_after_test):
    result = runner.invoke(app, ["create", "-n", "test", "-v", "--solver", "conda"])

    assert Path("test.yml").is_file()
    check_if_env_is_created("test")
    # from conda
    assert "Collecting package metadata (current_repodata.json):" in result.stdout


@pytest.mark.usefixtures("clean_up_env_after_test")
def test_create_w_pkg_install(clean_up_env_after_test):
    _ = runner.invoke(app, ["create", "-n", "test", "numpy"])

    assert Path("test.yml").is_file()
    check_if_env_is_created("test")
    check_if_pkg_is_installed("test", "numpy")
    check_if_pkgs_are_listed_in_specfile("test.yml", "numpy")


@pytest.mark.usefixtures("clean_up_env_after_test")
def test_create_w_pkg_install_w_channel(clean_up_env_after_test):
    result = runner.invoke(
        app, ["create", "-n", "test", "-c", "conda-forge", "python=3.9", "numpy"]
    )

    assert Path("test.yml").is_file()
    check_if_env_is_created("test")
    check_if_pkg_is_installed("test", "numpy", channel="conda-forge")
    check_if_pkgs_are_listed_in_specfile("test.yml", "numpy")
    check_if_channel_is_listed_in_specfile("test.yml", "conda-forge")


@pytest.mark.usefixtures("clean_up_env_after_test")
def test_create_env_from_yml_file(clean_up_env_after_test):
    result = runner.invoke(app, ["create", "--file", "tests/test-env.yml"])

    assert result.exit_code == 0
    check_if_env_is_created("test")
    check_if_pkg_is_installed("test", "python")


@pytest.mark.usefixtures("clean_up_env_after_test")
def test_create_env_from_lock_file(clean_up_env_after_test):
    _ = runner.invoke(
        app, ["create", "-n", "test", "-c", "conda-forge", "python=3.9", "typer"]
    )

    for file in os.listdir():
        if file.endswith(".lock") and file != "poetry.lock":
            lock_file = file

    result = runner.invoke(app, ["create", "--name", "test2", "--file", lock_file])

    check_if_env_is_created("test2")
    check_if_pkg_is_installed("test2", "typer", channel="conda-forge")


@pytest.mark.usefixtures("clean_up_env_after_test")
def test_env_creation_when_same_name_specfile_exists(clean_up_env_after_test):
    _ = runner.invoke(app, ["create", "-n", "test", "python=3.9"])

    # try to create a new env with same name
    _ = runner.invoke(app, ["create", "-n", "test", "python=3.9", "numpy"], input="y")
    # new env should have numpy and overwritten specfile
    check_if_pkg_is_installed("test", "numpy")
    check_if_pkgs_are_listed_in_specfile("test.yml", "numpy")
