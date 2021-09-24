from ezconda import __version__
from ezconda.main import app
from typer.testing import CliRunner


runner = CliRunner()


def test_version():
    result = runner.invoke(app, ["version"])
    assert __version__ == result.stdout.strip("\n")
