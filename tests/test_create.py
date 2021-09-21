import yaml
import subprocess
from typer.testing import CliRunner
from pathlib import Path
from ezconda.main import app


runner = CliRunner()


def clean_up_env_after_test(env_name: str) -> None:
    """Remove environment after each test runs"""
    subprocess.run(["conda", "env", "remove", "-n", env_name])
    subprocess.run(["rm", "-rf", f"{env_name}.yml"])


def test_create_without_install():
    result = runner.invoke(app, ["create", "-n", "test"])

    assert Path("test.yml").is_file()
    assert "Creating new conda environment" in result.stdout
    assert "Writing specifications to" in result.stdout
    clean_up_env_after_test("test")


def test_create_w_pkg_install():
    result = runner.invoke(app, ["create", "-n", "test", "numpy"])

    assert Path("test.yml").is_file()
    assert "Resolving packages..." in result.stdout
    # Test if the installed package is listed in the env.yml file
    with open("test.yml", "r") as f:
        env_specs = yaml.load(f, Loader=yaml.FullLoader)
        assert "numpy" in env_specs["dependencies"]

    clean_up_env_after_test("test")


def test_create_w_pkg_install_w_channel():
    result = runner.invoke(app, ["create", "-n", "test", "-c", "anaconda", "numpy"])

    assert Path("test.yml").is_file()
    assert "Resolving packages..." in result.stdout
    # Test if the installed package, channel name is listed in the env.yml file
    with open("test.yml", "r") as f:
        env_specs = yaml.load(f, Loader=yaml.FullLoader)
        assert "numpy" in env_specs["dependencies"]
        assert "anaconda" in env_specs["channels"]

    clean_up_env_after_test("test")
