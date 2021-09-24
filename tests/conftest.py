import pytest
import subprocess


@pytest.fixture()
def clean_up_env_after_test():
    yield
    """Remove environment after each test runs"""
    subprocess.run(["conda", "env", "remove", "-n", "test"])
    subprocess.run(["rm", "-rf", "test.yml"])
