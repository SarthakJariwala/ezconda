import sys
import subprocess
import json
import yaml


def check_if_env_is_created(env_name):
    envs = subprocess.run(
        ["conda", "env", "list", "--json"], capture_output=True, text=True
    )
    envs_dict = json.loads(envs.stdout)
    env_list = envs_dict["envs"]
    if sys.platform == "win32":
        env_list = [env.split("\\")[-1] for env in env_list]
    else:
        env_list = [env.split("/")[-1] for env in env_list]

    assert env_name in env_list


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


def check_if_pkgs_are_listed_in_specfile(specfile, pkgs):
    with open(specfile, "r") as f:
        env_specs = yaml.load(f, Loader=yaml.FullLoader)
        
        if not isinstance(pkgs, list):
            pkgs = [pkgs]
        
        for pkg in pkgs:
            assert pkg in env_specs["dependencies"]

def check_if_channel_is_listed_in_specfile(specfile, channel):
    with open(specfile, "r") as f:
        env_specs = yaml.load(f, Loader=yaml.FullLoader)
        
        assert channel in env_specs["channels"]
