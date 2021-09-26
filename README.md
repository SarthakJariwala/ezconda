# EZconda

Create and manage your conda environments. Create reproducible environments. No manual file edits for configurations.

[![Tests](https://github.com/SarthakJariwala/ezconda/workflows/Tests/badge.svg)](https://github.com/SarthakJariwala/ezconda/actions?workflow=Tests)
[![Codecov](https://codecov.io/gh/SarthakJariwala/ezconda/branch/master/graph/badge.svg)](https://codecov.io/gh/SarthakJariwala/ezconda)
[![PyPI](https://img.shields.io/pypi/v/ezconda.svg)](https://pypi.org/project/ezconda/)
[![Documentation Status](https://github.com/SarthakJariwala/ezconda/workflows/Docs/badge.svg)](https://sarthakjariwala.com/ezconda)

## Installation


<div class="termy">

```console
$ pip install ezconda
---> 100%
Successfully installed ezconda
```

</div>


## Create New Conda Environment

<div class="termy">

```console
// Create a new conda environment named 'ds-proj'
// The only change is 'ezconda'
$ ezconda create -n ds-proj python=3.9

// Creates 'ds-proj' env and installs python=3.9
Creating new conda environment : ds-proj ...
Resolving packages...

Done! You can activate it with :

        $ conda activate ds-proj

// Also creates a new YAML file with env specs
Writing specifications to ds-proj.yml ...
Created ds-proj.yml!

// Generates a lock file for identical env builds
Writing lock file... [EXPERIMENTAL]
Done!
```
</div>


!!! Note
    The only difference between from `ezconda` and `conda` commands that you type are the letters **`ez`**.

<div class="termy">

```console
// Let's take a look at environment file generated

$ cat ds-proj.yml

// Contents of ds-proj.yml
name: ds-proj
channels:
    - defaults
dependencies:
    - python=3.9

// Amazing! We didn't have to manually edit or generate it!
```

</div>


## Install Packages

<div class="termy">

```console
// Install numpy in 'ds-proj' from 'conda-forge'
$ ezconda install -n ds-proj -c conda-forge numpy

Validating file, packages, channels...
Installing packages...
Installation complete!

// Also updates environment YAML file
Updating ds-proj.yml...
Updated ds-proj.yml!

// Updates lock file for identical env builds
Writing lock file... [EXPERIMENTAL]
Done!
```
</div>

Let's take a look at the updated environment file

<div class="termy">

```console
$ cat ds-proj.yml

// Updated contents of ds-proj.yml
name: ds-proj
channels:
    - defaults
    - conda-forge
dependencies:
    - python=3.9
    - numpy

// It's updated! We didn't have to manually edit it!
```
</div>

!!! Note
    New packages (`numpy`) as well as channels (`conda-forge`) were added automatically to the `ds-proj.yml` file.

## Developing EZconda

### Run tests

```bash
docker-compose up --build test
```

### Local iterative development

```bash
docker-compose build dev && docker-compose run dev bash
```