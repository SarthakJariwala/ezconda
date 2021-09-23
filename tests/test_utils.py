import pytest
from typer.testing import CliRunner
from ezconda.main import app
from ezconda._utils import read_env_file


runner = CliRunner()


@pytest.mark.usefixtures("clean_up_env_after_test")
def test_read_env_file(clean_up_env_after_test):
    result = runner.invoke(app, ["create", "-n", "test"])
    env_specs = read_env_file("test.yml")
    
    EXPECTED_SPECS = {"name" : "test", "channels" : ["defaults"]}
    
    assert env_specs == EXPECTED_SPECS
