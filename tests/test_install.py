import pytest
from typer.testing import CliRunner
from ezconda.main import app


runner = CliRunner()


@pytest.mark.usefixtures("clean_up_env_after_test")
def test_install_w_no_existing_pkgs(clean_up_env_after_test):
    _ = runner.invoke(app, ["create", "-n", "test"])
    result = runner.invoke(app, ["install", "-n", "test", "python=3.8"])

    assert "Installed packages" in result.stdout
    assert "Updated specifications to 'test.yml'" in result.stdout


@pytest.mark.usefixtures("clean_up_env_after_test")
def test_verbose_install_w_conda(clean_up_env_after_test):
    _ = runner.invoke(app, ["create", "-n", "test"])
    result = runner.invoke(
        app, ["install", "-n", "test", "python=3.8", "-v", "--solver", "conda"]
    )

    assert "Collecting package metadata (current_repodata.json):" in result.stdout


@pytest.mark.usefixtures("clean_up_env_after_test")
def test_install_w_channel_and_no_existing_pkgs(clean_up_env_after_test):
    _ = runner.invoke(app, ["create", "-n", "test"])
    result = runner.invoke(
        app, ["install", "-n", "test", "-c", "conda-forge", "python=3.8"]
    )

    assert "Installed packages" in result.stdout
    assert "Updated specifications to 'test.yml'" in result.stdout


@pytest.mark.usefixtures("clean_up_env_after_test")
def test_install_with_existing_pkgs(clean_up_env_after_test):
    _ = runner.invoke(
        app, ["create", "-n", "test", "-c", "conda-forge", "python=3.8", "typer"]
    )
    result = runner.invoke(app, ["install", "-n", "test", "-c", "conda-forge", "numpy"])

    assert "Installed packages" in result.stdout
    assert "Updated specifications to 'test.yml'" in result.stdout


@pytest.mark.usefixtures("clean_up_env_after_test")
def test_install_an_existing_pkgs(clean_up_env_after_test):
    _ = runner.invoke(app, ["create", "-n", "test", "python=3.8", "typer"])
    result = runner.invoke(app, ["install", "-n", "test", "typer"])

    assert "'typer' already exists. Skipping installation." in result.stdout
