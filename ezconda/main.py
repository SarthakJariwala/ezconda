import yaml
from typing import List, Optional
from pathlib import Path
import typer
from conda.cli.python_api import run_command
from conda.cli.python_api import Commands


app = typer.Typer()


@app.command()
def create(
    name : str = typer.Option(..., "--name", "-n", help="Name of the environment to create"),
    packages : List[str] = typer.Argument(None, help="Additional packages to install"),
    channel: Optional[str] = typer.Option(None, "--channel", "-c", help="Additional channel to search for packages"),
    file : Optional[Path] = typer.Option(None, "--file", "-f", help="Name of the environment yaml file"),
    verbose : Optional[bool] = typer.Option(False, "--verbose", "-v", help="Display standard output from conda"),
):
    """
    Create a new conda environment and a corresponding YAML file containing environment details.
    """
    # check if file name exists
    if file is not None and file.is_file():
        typer.secho(f"{file} already exists! Please provide a different filename.", fg=typer.colors.BRIGHT_RED)
        raise typer.Exit()
    
    typer.secho(f"Creating new conda environment : {name} ...", fg=typer.colors.YELLOW)
    
    if packages:
       typer.secho(f"Adding packages to the environment...", fg=typer.colors.YELLOW)

    if not channel: 
        stdout, stderr, exit_code  = run_command(Commands.CREATE, "-n", name, *packages, use_exception_handler=True)
    else: # FIXME
        stdout, stderr, exit_code  = run_command(Commands.CREATE, "-n", name, "-channel", channel, *packages, use_exception_handler=True)
    
    if exit_code != 0:
        typer.secho(str(stdout + stderr), color=typer.colors.BRIGHT_RED)
        raise typer.Exit()
    
    if verbose:
        typer.echo(stdout)
    
    typer.secho(f"""Done! You can activate it with :         
    $ conda activate {name}
        """,
        fg=typer.colors.GREEN
    )

    if file is None:
        file = Path(f"{name}-env.yml")
    
    typer.secho(f"Writing to {file} ...", fg=typer.colors.GREEN)
    if file.is_file():
        overwrite = typer.confirm("There is an existing file. Do you want to update it?", abort=True)
        typer.secho(f"Updating {name}-env.yml ...", fg=typer.colors.YELLOW)
    
    env_specs = {}
    env_specs.update({"name" : name})
    if channel:
        env_specs.update({"channels" : [channel, "defaults"]})
    else:
        env_specs.update({"channels" : ["defaults"]})
    if packages:
        env_specs.update({"dependencies" : packages})
    
    with open(file, "w") as f:
        yaml.safe_dump(env_specs, f, sort_keys=False)
        
    typer.secho(f"Created {name}-env.yml!", fg=typer.colors.GREEN)
            
            




@app.command()
def install(
    pkg_name : List[str] = typer.Argument(..., help="Packages to install"),
    env_name : str = typer.Option(..., "--name", "-n", help="Name of the environment to install package into"),
    file : Optional[str] = typer.Option(None, "--file", "-f", help="env.yml file to update with new packages"),
    channel : Optional[str] = typer.Option(None, "--channel", "-c", help="Additional channel to search for packages"),
    verbose : Optional[bool] = typer.Option(False, "--verbose", "-v", help="Display standard output from conda")
):
    """Install conda package"""

    if not file:
        if not Path(f"{env_name}-env.yml").is_file():
            typer.secho(f"Couldn't find {env_name}-env.yml", fg=typer.colors.YELLOW)
            env_file = typer.prompt("Please provide the environment file to update")
            if Path(env_file).is_file():
                file = Path(env_file)
            else:
                typer.secho(f"Could not locate {env_file}'", fg=typer.colors.BRIGHT_RED)
                raise typer.Exit()
        else:
            file = Path(f"{env_name}-env.yml")

    with open(file, "r") as f:
        env_specs = yaml.load(f, Loader=yaml.FullLoader)
        existing_packages = env_specs["dependencies"]
        # check if packages already exists
        if existing_packages:
            for pkg in pkg_name:
                for ext_pkg in existing_packages:
                    if pkg in ext_pkg:
                        typer.secho(f"{pkg} already exists in {file}. Skipping installation. If you want to update {pkg}, use `update` instead.", fg=typer.colors.YELLOW)
                        raise typer.Exit()
    
            env_specs["dependencies"] = existing_packages + list(pkg_name)
        else:
            env_specs["dependencies"] = list(pkg_name)
    
    typer.secho("Installing packages...", fg=typer.colors.YELLOW)
    stdout, stderr, exit_code  = run_command(Commands.INSTALL, "-n", env_name, *pkg_name, use_exception_handler=True)
    
    if exit_code != 0:
        typer.secho(str(stdout + stderr), color=typer.colors.BRIGHT_RED)
        raise typer.Exit()
    
    if verbose:
        typer.echo(stdout)
    
    typer.secho("Installation complete!", fg=typer.colors.GREEN)
    typer.secho(f"Updating {file}...", fg=typer.colors.YELLOW)
    
    with open(file, "w") as f:
        yaml.safe_dump(env_specs, f, sort_keys=False)
    
    typer.secho(f"Updated {file}!", fg=typer.colors.GREEN)

@app.command()
def remove(name : str = typer.Argument(...)):
    stdout, stderr, exit_code  = run_command(Commands.REMOVE, "-n", name, use_exception_handler=True)
    typer.echo(stdout)



if __name__ == "__main__":
    app()