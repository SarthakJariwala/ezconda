import subprocess
import os
import sys
import platform
from typer.testing import CliRunner
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

    files = os.listdir()

    assert f"lock-test-{sys.platform}-{platform.machine()}.lock" in files

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

    subprocess.run(["rm", "-rf", f"lock-test-{sys.platform}-{platform.machine()}.lock"])
