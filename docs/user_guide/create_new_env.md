# Create New Environment

You can use the `create` command to create new conda environments with environment specifications file (more below).

## Create new (empty) environment

To create a new `conda` environment called `new-proj`:

<div class="termy">

```console
$ ezconda create -n new-proj

// Creates a new conda environment with name `new-proj`
🚀 Created 'new-proj' environment

⭐ Done!
```
</div>


## Create new environment with packages

Let's say you want to create a new `conda` environment called `new-proj` with `Python 3.9` installed.

<div class="termy">

```console
$ ezconda create -n new-proj python=3.9

// Creates a new conda environment with name `new-proj`
🚀 Created 'new-proj' environment

// Saves environment specs passed to `create` command (without any manual addition)
💾 Saved specifications to 'new-proj.yml'

// Generates an environment lock file
🔒 Lock file generated

⭐ Done!
```
</div>


Upon creating a new conda environment, **EZconda** also automatically creates a new specifications file `new-proj.yml`. As you can see below, the contents of the file contain the specifications entered above. 

```yaml title="new-proj.yml"
name: new-proj
channels:
    - defaults
dependencies:
    - python=3.9
```

Now, throughout the lifecycle of `new-proj` environment and your project, **EZconda** will manage this specifications file and update it as you make changes to the enironment.

!!! Tip
    Lock file generation is optional, but recommended for creating reproducible environment builds.
    
    You can disable it by passing `--no-lock` option.

!!! Note
    You can learn more about lock file [in the docs](recreate_env.md/#platform-specific-lock-files).


## Add channels

You can also add channels to the `create` command with `-c` or `-channel`, similar to the `conda create` command.

<div class="termy">

```console
$ ezconda create -n new-proj -c conda-forge python=3.9
```
</div>

The environment specification file, `new-proj.yml`,  now contains `conda-forge` in the channels section.

```YAML hl_lines="3" title="new-proj.yml"
name: new-proj
channels:
    - conda-forge
    - defaults
dependencies:
    - python=3.9
```

!!! Note

    The environment name `new-proj` is also the name of the environment specifcations file `new-proj.yml`.

    It is recommended to keep the environment name and specifications file name the same.
