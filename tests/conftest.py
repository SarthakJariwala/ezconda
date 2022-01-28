import imp
import pytest
import subprocess
import sys
import typer
from pathlib import Path


@pytest.fixture()
def clean_up_env_after_test():
    yield
    """Remove environment after each test runs"""
    subprocess.run(["conda", "env", "remove", "-n", "test"])
    subprocess.run(["rm", "-rf", "test.yml"])

    if sys.platform == "darwin":
        subprocess.run(["rm", "-rf", "test-osx-64.lock"])
    elif sys.platform == "win32":
        subprocess.run(["rm", "-rf", "test-win-64.lock"])
    elif sys.platform == "linux":
        subprocess.run(["rm", "-rf", "test-linux-64.lock"])


@pytest.fixture()
def delete_config_file():
    app_dir = typer.get_app_dir("ezconda")
    config_file: Path = Path(app_dir) / "config.json"
    yield
    """Remove config file after each test runs"""
    subprocess.run(["rm", "-rf", config_file])
