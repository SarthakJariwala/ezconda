import yaml
import subprocess
from typer.testing import CliRunner
from ezconda.main import app
from ezconda._utils import read_env_file


runner = CliRunner()


def clean_up_env_after_test(env_name: str) -> None:
    """Remove environment after each test runs"""
    subprocess.run(["conda", "env", "remove", "-n", env_name])
    subprocess.run(["rm", "-rf", f"{env_name}.yml"])


def test_read_env_file():
    result = runner.invoke(app, ["create", "-n", "test"])
    env_specs = read_env_file("test.yml")
    
    EXPECTED_SPECS = {"name" : "test", "channels" : ["defaults"]}
    
    assert env_specs == EXPECTED_SPECS
    clean_up_env_after_test("test")
