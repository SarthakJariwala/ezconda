import pytest
import subprocess
import sys


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
