from textwrap import dedent
import tomlkit
import sys
import json
import platform
import tempfile
import typer

from pathlib import Path
from typing import Dict, Optional

from tomlkit.toml_document import TOMLDocument

from ..console import console
from ..solver import Solver
from .._utils import run_command


class LockFile:

    _MIN_EZCONDA_VERSION = "0.4.0"

    def __init__(self) -> None:

        self.doc = TOMLDocument()

    def _add_version_info(self) -> None:

        version = tomlkit.table()
        version.add("ezconda-min-version", self._MIN_EZCONDA_VERSION)

        self.doc.add("version", version)

    def _add_system_info(self) -> None:

        system = tomlkit.table()
        system.add("platform", sys.platform)
        system.add("architecture", platform.architecture()[0])
        system.add("machine", platform.machine())

        self.doc.add("system", system)

    def _add_current_packages(self, env_name: str) -> Dict:
        """Get current installed packages in the named environment"""

        cmd = ["conda", "list", "-n", env_name, "--json"]

        result = run_command(cmd, verbose=False)

        packages = json.loads(result.stdout)

        # store environment name
        _env_table = tomlkit.table()
        _env_table.add("name", env_name)

        self.doc.add("environment", _env_table)
        self.doc.add("packages", packages)

    def generate_lockfile(self, env_name: str) -> None:

        self._add_version_info()
        self._add_system_info()
        self._add_current_packages(env_name)

    def write_lockfile(self, env_name: str) -> None:

        self.generate_lockfile(env_name)

        lockfile_name = f"{env_name}-{sys.platform}-{platform.machine()}.lock"

        with open(lockfile_name, "w") as f:
            tomlkit.dump(self.doc, f)

        console.print(f"[bold green] :lock: Lock file '{lockfile_name}' generated")

    def read_lock_file(self, lock_file: Path) -> TOMLDocument:

        with open(lock_file, "r") as f:
            doc = tomlkit.loads(f.read())
        return doc

    def verify_lock_file_contents(self, doc: TOMLDocument) -> None:

        # check contents
        if "version" not in doc or "system" not in doc:
            console.print(
                dedent(
                    """
                    [bold red]Lock file is missing fields and incorrect.[/]
                    
                    To correct and regenerate a new lock file:

                    [bold green]ezconda lock -n <environment_name>[/]

                    If the environment does not exist on your system,
                    you can create it using the corresponding '.yml' file:

                    [bold green]ezconda create -n <environment_name> -f <env.yml>[/]
                    """
                )  # TODO: add creating env from yml file
            )
            raise typer.Exit()

        # get system info from lock file
        system = doc["system"]

        # get current system info
        _current_system = {
            "platform": sys.platform,
            "architecture": platform.architecture()[0],
            "machine": platform.machine(),
        }

        if system != _current_system:
            console.print(
                dedent(
                    f"""
                    :heavy_exclamation_mark:[bold red]Incompatible lock file.[/]

                    Lock file was generated on [bold green]{system["platform"]}-{system["machine"]}[/].

                    Current system is [bold yellow]{_current_system["platform"]}-{_current_system["machine"]}[/].
                    """
                )
            )
            raise typer.Exit()


def read_lock_file_and_install(
    lock_file: Path,
    solver: Solver,
    verbose: bool,
    env_name: Optional[str] = None,
) -> str:
    """
    Reads lock file, verifies the content and creates a new environment
    with packages specifed in the lock file and returns the environment name.
    """

    with console.status(f"[magenta]Reading lock file") as status:

        l = LockFile()
        complete_specs = l.read_lock_file(lock_file)

        l.verify_lock_file_contents(complete_specs)

        if env_name is None:
            env_name = complete_specs["environment"]["name"]

        explicit_specs = [
            f"{pkg['base_url']}/{pkg['platform']}/{pkg['dist_name']}"
            for pkg in complete_specs["packages"]
            if not pkg["channel"].startswith("pypi")
        ]

        explicit_specs = [
            spec + ".conda"
            if spec.startswith("https://repo.anaconda.com")
            else spec + ".tar.bz2"
            for spec in explicit_specs
        ]

        with tempfile.NamedTemporaryFile() as f:
            f.write(bytes("@EXPLICIT\n", "utf-8"))
            f.writelines([bytes(specs + "\n", "utf-8") for specs in explicit_specs])
            f.flush()

            status.update(f"[magenta]Creating new conda environment {env_name}")

            cmd = [
                f"{solver.value}",
                "create",
                "-n",
                env_name,
                "--file",
                f"{f.name}",
                "-y",
            ]

            result = run_command(cmd, verbose=verbose)

        # TODO: Add installation for pypi channels/packages

        console.print(
            f"[bold green] :rocket: Created '{env_name}' environment from lock file",
        )
    
    return env_name
