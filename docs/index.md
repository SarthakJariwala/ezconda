# EZconda

![EZconda](logo.png)

<p align="center">
    <a href="https://github.com/SarthakJariwala/ezconda/actions?workflow=Tests">
        <img src="https://github.com/SarthakJariwala/ezconda/workflows/Tests/badge.svg">
    </a>
    <a href="https://codecov.io/gh/SarthakJariwala/ezconda">
        <img src="https://codecov.io/gh/SarthakJariwala/ezconda/branch/main/graph/badge.svg">
    </a>
    <a href="https://anaconda.org/conda-forge/ezconda">
        <img alt="Conda (channel only)" src="https://img.shields.io/conda/vn/conda-forge/ezconda">
    </a>
    <a href="https://ezconda.sarthakjariwala.com">
        <img src="https://github.com/SarthakJariwala/ezconda/workflows/Docs/badge.svg">
    </a>
</p>

<p align="center">
    <em><b>Create, Manage, Re-create</b> conda environments & specifications with ease.</em>
</p>

---

**EZconda** is a command line interface application that helps practitioners create and manage `conda` environment and related specifications with ease.

> It provides an easy to use higher level abstraction for creating and managing reproducible `conda` environments.

## Key Features

- **Environment Management** : Create and manage `conda` environments with ease.

- **Specifications Management** : Add and remove packages from the <abbr title="commonly known as environment.yml file">specifications file</abbr> as you install & remove them.
    
    > _**No manual file edits! No exporting entire environments!**_

- **Reproducible Environments** : Auto lock current environment state and re-create it exactly anywhere!

- **Easy & Intuitive** : Intuitive commands and autocompletions by default.

- **Fast & Reliable Environment Resolution** : Get fast and reliable environment solves by default.

    > *EZconda* uses `mamba` by default, but you can easily switch between `mamba` and `conda`.

- **Built-in Good Practices & Guardrails** : Enables the user to follow good practices, by default.

## Requirements

Requires a [conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html) installation.

## Installation

The recommended way to install **EZconda** is using `conda` or `mamba` in the `base` environment : 

### Using `conda`

<div class="termy">

```console
$ conda install ezconda -c conda-forge -n base
---> 100%
Successfully installed ezconda
```

</div>

### Using `mamba`

<div class="termy">

```console
$ mamba install ezconda -c conda-forge -n base
---> 100%
Successfully installed ezconda
```

</div>

??? Info "mamba"
    If you haven't heard of `mamba`, it offers higher speed and more reliable environment solutions. Learn more about `mamba` on their [website](https://mamba.readthedocs.io/en/latest/).

## A Minimal Example

### Create a new environment

Create a new environment with `Python 3.9` installed -

<div class="termy">

```console
$ ezconda create -n ds-proj python=3.9

// Creates ds-proj with Python=3.9 installed
```

</div>

**EZconda** creates the `conda` environment as well as a specifications file `ds-proj.yml` (named after the environment name) -

```YAML title="ds-proj.yml" hl_lines="1 5" 
name: ds-proj
channel:
    - defaults
dependencies:
    - python=3.9
```

### Install packages

As you install packages, the specifications file is also updated accordingly.

<div class="termy">

```console
$ ezconda install -n ds-proj -c conda-forge numpy pandas scipy
// Installs numpy, scipy, pandas from conda-forge channel
```

</div>

```YAML title="ds-proj.yml" hl_lines="3 7-9" 
name: ds-proj
channel:
    - conda-forge
    - defaults
dependencies:
    - python=3.9
    - numpy
    - pandas
    - scipy
```

!!! Note "Adding channels"
    The `conda-forge` channel was also added to the specifications along with the packages.

### Remove packages

The specifications file is also updated when you remove packages.

<div class="termy">

```console
$ ezconda remove -n ds-proj pandas
// Removes pandas from ds-proj
```

</div>

```YAML title="ds-proj.yml" hl_lines="7 8" 
name: ds-proj
channel:
    - conda-forge
    - defaults
dependencies:
    - python=3.9
    - numpy
    - scipy
```

!!! Note "Informed Package Removal"
    If you try to remove a package that is a dependency for an installed package, **EZconda** will inform you before removing the package. See [docs](user_guide/remove_packages.md) for more details.

### Sync environment with changes

Let's say you are working with collaborators and they update the specifications file (`ds-proj.yml`) with a new dependency. Now, your local conda environment is out of sync with the new dependencies. 

To bring it back in sync, you can use the `sync` command.

<div class="termy">

```console
$ ezconda sync -n ds-proj --with specfile

// Syncs ds-proj environment with new changes in specifications file (ds-proj.yml)
```
</div>

!!! Info "Sync changes"
    Learn more about syncing environments in the [user guide](./user_guide/sync_env.md).

### Re-create environment

As you create, install and remove packages, in addition to the specifications file, **EZconda** also generates and maintains a lock file.

You can use this lock file to reproducibly re-create an environment.

!!! Info "Lock file"
    You can learn more about [reproducible environments](./design_decisions/reproducible_environments.md) and [lock file](./design_decisions/lockfile.md) in docs.

<div class="termy">

```console
$ ezconda create --file ds-proj-darwin-x86_64.lock

// Creates a new environment 'ds-proj-darwin-x86_64.lock'
```
</div>


## Summary

In summary, **EZconda** provides an easy to use higher level abstraction for creating and managing reproducible `conda` environments.

To learn more, check out the [User Guide](user_guide/create_new_env.md)