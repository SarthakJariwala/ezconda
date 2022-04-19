import sys
import subprocess
import json
import yaml
import pytest
from typer.testing import CliRunner
from pathlib import Path
from ezconda.main import app


runner = CliRunner()


@pytest.mark.usefixtures("clean_up_env_after_test")
def test_create_without_install(clean_up_env_after_test):
    result = runner.invoke(app, ["create", "-n", "test"])

    assert Path("test.yml").is_file()
    assert "Created 'test' environment" in result.stdout
    assert "Saved specifications to 'test.yml'" in result.stdout


@pytest.mark.usefixtures("clean_up_env_after_test")
def test_verbose_w_conda(clean_up_env_after_test):
    result = runner.invoke(app, ["create", "-n", "test", "-v", "--solver", "conda"])

    assert Path("test.yml").is_file()
    # from conda
    assert "Collecting package metadata (current_repodata.json):" in result.stdout

    assert "Created 'test' environment" in result.stdout
    assert "Saved specifications to 'test.yml'" in result.stdout


@pytest.mark.usefixtures("clean_up_env_after_test")
def test_create_w_pkg_install(clean_up_env_after_test):
    result = runner.invoke(app, ["create", "-n", "test", "numpy"])

    assert Path("test.yml").is_file()
    assert "Created 'test' environment" in result.stdout
    assert "Saved specifications to 'test.yml'" in result.stdout
    # Test if the installed package is listed in the env.yml file
    with open("test.yml", "r") as f:
        env_specs = yaml.load(f, Loader=yaml.FullLoader)
        assert "numpy" in env_specs["dependencies"]


@pytest.mark.usefixtures("clean_up_env_after_test")
def test_create_w_pkg_install_w_channel(clean_up_env_after_test):
    result = runner.invoke(app, ["create", "-n", "test", "-c", "anaconda", "numpy"])

    assert Path("test.yml").is_file()
    assert "Created 'test' environment" in result.stdout
    assert "Saved specifications to 'test.yml'" in result.stdout
    # Test if the installed package, channel name is listed in the env.yml file
    with open("test.yml", "r") as f:
        env_specs = yaml.load(f, Loader=yaml.FullLoader)
        assert "numpy" in env_specs["dependencies"]
        assert "anaconda" in env_specs["channels"]


@pytest.mark.usefixtures("clean_up_env_after_test")
def test_create_env_from_yml_file(clean_up_env_after_test):
    result = runner.invoke(app, ["create", "--file", "tests/test-env.yml"])

    p = subprocess.run(
        ["conda", "env", "list", "--json"],
        capture_output=True,
        text=True,
    )
    env_dict = json.loads(p.stdout)
    if sys.platform == "win32":
        envs = [env.split("\\")[-1] for env in env_dict["envs"]]
    else:
        envs = [env.split("/")[-1] for env in env_dict["envs"]]

    assert "test" in envs
