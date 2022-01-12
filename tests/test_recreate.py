import sys
import os
import json
import pytest
from typer.testing import CliRunner
from ezconda.main import app


runner = CliRunner()


@pytest.mark.usefixtures("clean_up_env_after_test")
def test_recreate_env_with_not_a_file(clean_up_env_after_test):
    result = runner.invoke(app, ["recreate", "non_existing_file"])

    assert "non_existing_file is not a valid file" in result.stdout


@pytest.mark.usefixtures("clean_up_env_after_test")
def test_recreate_wo_env_name(clean_up_env_after_test):
    _ = runner.invoke(
        app, ["create", "-n", "test", "-c", "conda-forge", "python=3.9", "typer"]
    )

    for file in os.listdir():
        if file.endswith(".lock") and file != "poetry.lock":
            lock_file = file
    result = runner.invoke(app, ["recreate", lock_file])

    assert f"Installed all dependencies from '{lock_file}'" in result.stdout

    # check if env is created
    env_name = lock_file.strip('.lock')
    envs_installed = json.load(os.popen("conda env list --json"))["envs"]
    if sys.platform == "darwin":
        assert f"/usr/local/miniconda/envs/{env_name}" in envs_installed
    else:
        assert f"/usr/share/miniconda/envs/{env_name}" in envs_installed

    # check if typer is installed in the env
    pkgs = json.load(os.popen(f"conda list -n {env_name} --json"))
    for pkg in pkgs:
        if pkg == "typer":
            assert pkg["name"] == "typer"
            assert pkg["channel"] == "conda-forge"


@pytest.mark.usefixtures("clean_up_env_after_test")
def test_recreate_w_env_name(clean_up_env_after_test):
    _ = runner.invoke(
        app, ["create", "-n", "test", "-c", "conda-forge", "python=3.9", "typer"]
    )

    for file in os.listdir():
        if file.endswith(".lock") and file != "poetry.lock":
            lock_file = file
    env_name = "test2"
    result = runner.invoke(app, ["recreate", lock_file, "-n", env_name])

    assert f"Installed all dependencies from '{lock_file}'" in result.stdout

    # check if env is created
    envs_installed = json.load(os.popen("conda env list --json"))["envs"]
    if sys.platform == "darwin":
        assert f"/usr/local/miniconda/envs/{env_name}" in envs_installed
    else:
        assert f"/usr/share/miniconda/envs/{env_name}" in envs_installed

    # check if typer is installed in the env
    pkgs = json.load(os.popen(f"conda list -n {env_name} --json"))
    for pkg in pkgs:
        if pkg["name"] == "typer":
            assert pkg["name"] == "typer"
            assert pkg["channel"] == "conda-forge"
