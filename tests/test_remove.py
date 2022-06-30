import pytest
from typer.testing import CliRunner
from ezconda.main import app
from .helpers import check_if_pkg_is_installed


runner = CliRunner()


@pytest.mark.usefixtures("clean_up_env_after_test")
def test_remove_single_pkg(clean_up_env_after_test):
    _ = runner.invoke(
        app, ["create", "-n", "test", "-c", "conda-forge", "python=3.8", "typer"]
    )
    result = runner.invoke(app, ["remove", "-n", "test", "typer"])

    assert "Removed packages from test" in result.stdout
    assert "Updated specifications in 'test.yml'" in result.stdout


@pytest.mark.usefixtures("clean_up_env_after_test")
def test_remove_multiple_pkgs(clean_up_env_after_test):
    _ = runner.invoke(
        app,
        ["create", "-n", "test", "-c", "conda-forge", "python=3.8", "typer", "numpy"],
    )
    result = runner.invoke(app, ["remove", "-n", "test", "typer", "numpy"])

    assert "Removed packages from test" in result.stdout
    assert "Updated specifications in 'test.yml'" in result.stdout


@pytest.mark.usefixtures("clean_up_env_after_test")
def test_remove_an_non_existant_pkg(clean_up_env_after_test):
    _ = runner.invoke(
        app,
        [
            "create",
            "-n",
            "test",
            "python=3.8",
        ],
    )
    result = runner.invoke(app, ["remove", "-n", "test", "typer"])

    assert "'typer' is not listed in 'test.yml' file!" in result.stdout


@pytest.mark.usefixtures("clean_up_env_after_test")
def test_remove_a_pkg_that_is_a_dep_for_other(clean_up_env_after_test):
    _ = runner.invoke(
        app,
        ["create", "-n", "test", "-c", "conda-forge", "python=3.9", "numpy", "pandas"],
    )

    # remove numpy which is a dep of pandas and say "yes" at prompt
    _ = runner.invoke(app, ["remove", "-n", "test", "numpy"], input="y")

    # should remove both numpy and pandas
    with pytest.raises(AssertionError):
        check_if_pkg_is_installed("test", "numpy", "conda-forge")
        check_if_pkg_is_installed("test", "pandas", "conda-forge")
