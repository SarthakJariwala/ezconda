import yaml
import pytest
from typer.testing import CliRunner
from pathlib import Path
from ezconda.main import app


runner = CliRunner()


@pytest.mark. usefixtures("clean_up_env_after_test")
def test_create_without_install(clean_up_env_after_test):
    result = runner.invoke(app, ["create", "-n", "test"])

    assert Path("test.yml").is_file()
    assert "Creating new conda environment" in result.stdout
    assert "Writing specifications to" in result.stdout


@pytest.mark. usefixtures("clean_up_env_after_test")
def test_verbose(clean_up_env_after_test):
    result = runner.invoke(app, ["create", "-n", "test", "-v"])

    assert Path("test.yml").is_file()
    assert "Creating new conda environment" in result.stdout
    # from conda
    assert "Collecting package metadata (current_repodata.json):" in result.stdout


@pytest.mark.usefixtures("clean_up_env_after_test")
def test_create_w_pkg_install(clean_up_env_after_test):
    result = runner.invoke(app, ["create", "-n", "test", "numpy"])

    assert Path("test.yml").is_file()
    assert "Resolving packages..." in result.stdout
    # Test if the installed package is listed in the env.yml file
    with open("test.yml", "r") as f:
        env_specs = yaml.load(f, Loader=yaml.FullLoader)
        assert "numpy" in env_specs["dependencies"]



@pytest.mark.usefixtures("clean_up_env_after_test")
def test_create_w_pkg_install_w_channel(clean_up_env_after_test):
    result = runner.invoke(app, ["create", "-n", "test", "-c", "anaconda", "numpy"])

    assert Path("test.yml").is_file()
    assert "Resolving packages..." in result.stdout
    # Test if the installed package, channel name is listed in the env.yml file
    with open("test.yml", "r") as f:
        env_specs = yaml.load(f, Loader=yaml.FullLoader)
        assert "numpy" in env_specs["dependencies"]
        assert "anaconda" in env_specs["channels"]

