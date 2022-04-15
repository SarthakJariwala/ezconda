from unittest import runner
import pytest
import subprocess
from typer.testing import CliRunner
from ezconda.main import app
from ezconda.summary import get_summary_for_revision


runner = CliRunner()

@pytest.mark.usefixtures("clean_up_env_after_test")
def test_index_error(clean_up_env_after_test):
    _ = runner.invoke(app, ["create", "-n", "test", "python=3.8"])
    # test a revision number that does not exist
    result = runner.invoke(app, ["summary", "-n", "test", "--revision", "20"])
    assert result.exit_code == 1

@pytest.mark.usefixtures("clean_up_env_after_test")
def test_installs_upgrade_downgrade_removal_summary(clean_up_env_after_test):
    # install packages from defaults channel
    _ = runner.invoke(app, ["create", "-n", "test", "python=3.8"])
    # now install from conda-forge channel
    _ = runner.invoke(app, ["install", "-n", "test", "-c", "conda-forge", "numpy"])
    # test if summary has install, upgrade, downgrade
    install, upgrade, downgrade, removal = get_summary_for_revision("test", revision_no=-1)
    # check if returns are empty
    assert install
    assert upgrade
    assert downgrade
    # now remove numpy
    _ = runner.invoke(app, ["remove", "-n", "test", "numpy"])
    # test if remove is not empty
    install, upgrade, downgrade, removal = get_summary_for_revision("test", revision_no=-1)
    assert removal
