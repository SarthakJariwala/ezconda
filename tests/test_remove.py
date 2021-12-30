import pytest
from typer.testing import CliRunner
from ezconda.main import app


runner = CliRunner()


@pytest.mark.usefixtures("clean_up_env_after_test")
def test_remove_single_pkg(clean_up_env_after_test):
    _ = runner.invoke(
        app, ["create", "-n", "test", "-c", "conda-forge", "python=3.8", "typer"]
    )
    result = runner.invoke(app, ["remove", "-n", "test", "typer"])

    assert "Removed packages from test" in result.stdout
    assert "Saved specifications to 'test.yml'" in result.stdout


@pytest.mark.usefixtures("clean_up_env_after_test")
def test_remove_multiple_pkgs(clean_up_env_after_test):
    _ = runner.invoke(
        app,
        ["create", "-n", "test", "-c", "conda-forge", "python=3.8", "typer", "numpy"],
    )
    result = runner.invoke(app, ["remove", "-n", "test", "typer", "numpy"])

    assert "Removed packages from test" in result.stdout
    assert "Saved specifications to 'test.yml'" in result.stdout


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


# @pytest.mark.usefixtures("clean_up_env_after_test")
# def test_remove_a_pkg_that_is_a_dep_for_other(clean_up_env_after_test):
#     _ = runner.invoke(
#         app,
#         ["create", "-n", "test", "-c", "conda-forge", "python=3.8", "numpy", "pandas"],
#     )
#     result = runner.invoke(app, ["remove", "-n", "test", "numpy"])

#     assert "There are packages that depend on ('numpy',)" in result.stdout
#     assert "Removing ('numpy',) will also remove the following" in result.stdout
