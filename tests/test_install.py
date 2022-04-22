import subprocess
import json
import pytest
from typer.testing import CliRunner
from ezconda.main import app


runner = CliRunner()


def check_if_pkg_is_installed(env_name, pkg_name, channel=None):
    pkg_specs = subprocess.run(
        ["conda", "list", "-n", env_name, "--json"], capture_output=True
    )
    pkg_specs = json.loads(pkg_specs.stdout)

    list_of_pkgs = [pkg["name"] for pkg in pkg_specs]
    assert pkg_name in list_of_pkgs

    if channel:
        for pkg in pkg_specs:
            if pkg["name"] == pkg_name:
                assert pkg["channel"] == channel


@pytest.mark.usefixtures("clean_up_env_after_test")
def test_install_w_no_existing_pkgs(clean_up_env_after_test):
    _ = runner.invoke(app, ["create", "-n", "test"])
    result = runner.invoke(app, ["install", "-n", "test", "python=3.8"])

    assert result.exit_code == 0

    check_if_pkg_is_installed("test", "python")


@pytest.mark.usefixtures("clean_up_env_after_test")
def test_verbose_install_w_conda(clean_up_env_after_test):
    _ = runner.invoke(app, ["create", "-n", "test"])
    result = runner.invoke(
        app, ["install", "-n", "test", "python=3.8", "-v", "--solver", "conda"]
    )

    assert "Collecting package metadata (current_repodata.json):" in result.stdout

    assert result.exit_code == 0

    check_if_pkg_is_installed("test", "python")


@pytest.mark.usefixtures("clean_up_env_after_test")
def test_install_w_channel_and_no_existing_pkgs(clean_up_env_after_test):
    _ = runner.invoke(app, ["create", "-n", "test"])
    result = runner.invoke(
        app, ["install", "-n", "test", "-c", "conda-forge", "python=3.8"]
    )

    assert result.exit_code == 0

    check_if_pkg_is_installed("test", "python", channel="conda-forge")


@pytest.mark.usefixtures("clean_up_env_after_test")
def test_install_with_existing_pkgs(clean_up_env_after_test):
    _ = runner.invoke(
        app, ["create", "-n", "test", "-c", "conda-forge", "python=3.8", "typer"]
    )
    result = runner.invoke(app, ["install", "-n", "test", "-c", "conda-forge", "numpy"])

    assert result.exit_code == 0

    # check if numpy is installed from conda-forge channel
    check_if_pkg_is_installed("test", "numpy", "conda-forge")


@pytest.mark.usefixtures("clean_up_env_after_test")
def test_install_an_existing_pkgs(clean_up_env_after_test):
    _ = runner.invoke(app, ["create", "-n", "test", "python=3.8", "typer"])
    result = runner.invoke(app, ["install", "-n", "test", "typer"])

    assert "'typer' already exists. Skipping installation." in result.stdout
