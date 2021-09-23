import pytest
from typer.testing import CliRunner
from ezconda.main import app
from ezconda._utils import (
    read_env_file,
    create_initial_env_specs,
    add_pkg_to_dependencies,
    add_new_channel_to_env_specs,
    remove_pkg_from_dependencies
)


runner = CliRunner()


@pytest.mark.usefixtures("clean_up_env_after_test")
def test_read_env_file(clean_up_env_after_test):
    result = runner.invoke(app, ["create", "-n", "test"])
    env_specs = read_env_file("test.yml")
    
    EXPECTED_SPECS = {"name" : "test", "channels" : ["defaults"]}
    
    assert env_specs == EXPECTED_SPECS


@pytest.mark.parametrize(
    "env_name,channel,packages,expected",
    [
        ("test", None, None, {"name" : "test", "channels" : ["defaults"]}),
        ("test", "conda-forge", None, {"name" : "test", "channels" : ["conda-forge", "defaults"]}),
        ("test", "anaconda", ["numpy"], {"name" : "test", "channels" : ["anaconda", "defaults"], "dependencies" : ["numpy"]}),
        ("test", "anaconda", ["numpy", "scipy"], {"name" : "test", "channels" : ["anaconda", "defaults"], "dependencies" : ["numpy", "scipy"]}),
    ]
)
def test_create_initial_env_specs(env_name, channel, packages, expected):
    env_specs = create_initial_env_specs(env_name, channel, packages)

    assert env_specs == expected


@pytest.mark.parametrize(
    "ENV_SPECS,package,EXPECTED_SPECS",
    [
        (
            {"name" : "test", "channels" : ["conda-forge", "defaults"], "dependencies" : ["numpy", "scipy"]},
            ["matplotlib"],
            {"name" : "test", "channels" : ["conda-forge", "defaults"], "dependencies" : ["numpy", "scipy", "matplotlib"]}
        ),
        (
            {"name" : "test", "channels" : ["conda-forge", "defaults"], "dependencies" : ["numpy", "scipy"]},
            ["matplotlib", "pandas"],
            {"name" : "test", "channels" : ["conda-forge", "defaults"], "dependencies" : ["numpy", "scipy", "matplotlib", "pandas"]}
        ),
        (   # if there are no existing pacakges
            {"name" : "test", "channels" : ["conda-forge", "defaults"]},
            ["matplotlib", "pandas"],
            {"name" : "test", "channels" : ["conda-forge", "defaults"], "dependencies" : ["matplotlib", "pandas"]}
        ),
    ]
)
def test_add_pkg_to_dependencies(ENV_SPECS, package, EXPECTED_SPECS):
    env_specs = add_pkg_to_dependencies(ENV_SPECS, package)
    
    assert env_specs == EXPECTED_SPECS


@pytest.mark.parametrize(
    "ENV_SPECS,channel,EXPECTED_SPECS",
    [
        (   # if channel already exists
            {"name" : "test", "channels" : ["defaults", "conda-forge"]},
            "conda-forge",
            {"name" : "test", "channels" : ["defaults", "conda-forge"]}
        ),
        (   # if channel does not exist
            {"name" : "test", "channels" : ["defaults"]},
            "conda-forge",
            {"name" : "test", "channels" : ["defaults", "conda-forge"]}
        ),
        (   # if there are no specified channels
            {"name" : "test", "channels" : ["conda-forge", "defaults"]},
            None,
            {"name" : "test", "channels" : ["conda-forge", "defaults"]}
        ),
    ]
)
def test_add_new_channel_to_env_specs(ENV_SPECS, channel, EXPECTED_SPECS):
    env_specs = add_new_channel_to_env_specs(ENV_SPECS, channel)
    
    assert env_specs == EXPECTED_SPECS


@pytest.mark.parametrize(
    "ENV_SPECS,package,EXPECTED_SPECS",
    [
        (
            {"name" : "test", "channels" : ["conda-forge", "defaults"], "dependencies" : ["numpy", "scipy", "matplotlib"]},
            ["matplotlib"],
            {"name" : "test", "channels" : ["conda-forge", "defaults"], "dependencies" : ["numpy", "scipy"]}
        ),
        (
            {"name" : "test", "channels" : ["conda-forge", "defaults"], "dependencies" : ["numpy", "scipy", "matplotlib", "pandas"]},
            ["matplotlib", "pandas"],
            {"name" : "test", "channels" : ["conda-forge", "defaults"], "dependencies" : ["numpy", "scipy"]}
        ),
    ]
)
def test_remove_pkg_from_dependencies(ENV_SPECS, package, EXPECTED_SPECS):
    env_specs = remove_pkg_from_dependencies(ENV_SPECS, package)
    
    assert env_specs == EXPECTED_SPECS