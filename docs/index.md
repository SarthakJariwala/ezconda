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

## Key Features

- **Environment specifications** : Add & remove packages from the <abbr title="commonly known as environment.yml file">specifications file</abbr> as you install & remove packages. _**No manual file edits!**_

- **Environment management** : Create & manage `conda` environments with ease.

- **Reproducible environments** : Lock current environment state and re-create it when necessary.

- **Easy to use & intuitive** : It very closely mimics `conda` API, so there is no new API to learn for users. Autocomplete for all shells.

- **Fast & Reliable Environment resolution** : Get fast and reliable environment solves by default. *EZconda* uses `mamba` by default, but you can easily switch between `mamba` and `conda`.

- **Best practices built-in** : Enforces the user to follow best `conda` practices.

## Requirements

Requires a [conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html) installation.

## Installation

The recommended way to install **EZconda** is using `conda` or `mamba` in the `base` environment : 

### Using `conda`: 

<div class="termy">

```console
$ conda install ezconda -c conda-forge -n base
---> 100%
Successfully installed ezconda
```

</div>

### Using `mamba`:

<div class="termy">

```console
$ mamba install ezconda -c conda-forge -n base
---> 100%
Successfully installed ezconda
```

</div>

!!! Info
    If you haven't heard of `mamba`, it offers higher speed and more reliable environment solutions. Learn more about `mamba` on their [website](https://mamba.readthedocs.io/en/latest/).

## A Minimal Example

### Create a new environment

Create a new environment with `Python 3.9` installed -

<div class="termy">

```console
$ ezconda create -n ds-proj python=3.9
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

### Recreate environment

As you create, install and remove packages, in addition to the specifications file, **EZconda** also generates and maintains a lock file. You can use this lock file to reproducibly recreate an environment.

<div class="termy">

```console
$ ezconda recreate -n new-env ds-proj-osx-64.lock

// Creates a new environment 'new-env' that is identical to 'ds-proj'
```
</div>

!!! Info "Lock file"
    You can learn more about environment recreation in the [docs](user_guide/recreate_env.md).

## Summary

In summary, **EZconda** creates a specifications file and a lock file for you as you create and manage your conda environment and packages.

To learn more, check out the [User Guide](user_guide/create_new_env.md)