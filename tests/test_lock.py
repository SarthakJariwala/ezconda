import subprocess
import os
import sys
import pytest
from typer.testing import CliRunner
from pathlib import Path
from ezconda.main import app


runner = CliRunner()

def test_lock_for_existing_conda_envs():
    _ = subprocess.run(
            [
                "conda",
                "create",
                "-n",
                "lock-test",
                "python=3.9",
                "-y",
            ]
        )
    p = runner.invoke(app, ["lock", "-n", "lock-test"])

    assert "Lock file generated" in p.stdout
    
    files = os.listdir()
    print(files)
    for f in files:
        if f.endswith(".lock") and f != "poetry.lock":
            if f.startswith(f"test-{sys.platform}"): 
                pass
            else:
                assert f.startswith("lock-test") == True
    
    _ = subprocess.run(
            [
                "conda",
                "env",
                "remove",
                "-n",
                "lock-test",
                "-y",
            ]
        )
    
    if sys.platform == "darwin":
        subprocess.run(["rm", "-rf", "lock-test-osx-64.lock"])
    elif sys.platform == "win32":
        subprocess.run(["rm", "-rf", "lock-test-win-64.lock"])
    elif sys.platform == "linux":
        subprocess.run(["rm", "-rf", "lock-test-linux-64.lock"])