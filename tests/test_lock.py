import subprocess
import os
import sys
import pytest
from typer.testing import CliRunner
from pathlib import Path
from ezconda.main import app


runner = CliRunner()


def test_lock_for_existing_conda_envs():
    subprocess.run(
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

    assert " 🔒 Lock file" in p.stdout

    files = os.listdir()

    if sys.platform == "darwin":
        assert "lock-test-osx-64.lock" in files
    elif sys.platform == "win32":
        assert "lock-test-win-64.lock" in files
    else:
        assert "lock-test-linux-64.lock" in files

    subprocess.run(
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
