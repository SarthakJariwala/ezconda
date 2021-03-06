# Specifications File

This file is similar to the `environment.yml` file in `conda`.

However, the big difference is, it only tracks the dependencies that the [user sepcifies at the command line.](#user-specified-packages) and not its dependencies.

??? Info
    An exhaustive description of the pacakges and its dependencies is in the [lock file](lockfile.md).

## Format

The specifications file format is similar to `conda` environment specifications files. This is primarily done to maintain compatibility with `conda`.

In other words, you can use this specifications file generated by `ezconda` with `conda`.

It specifies the packages (and not their dependencies) and channels of interest -

```YAML title="mlproj.yml"
# name of the environment
name: mlproj

# channels to search
channels:
    - defaults
    - conda-forge

# packages to install
packages:
    - python=3.8
    - numpy>=1.17
    - pandas
```

!!! Note
    You _**do not**_ need to add or remove packages manually from the environment.yml file.

    This is done **automatically** when you install/remove packages using ezconda. See [user guide](../user_guide/install_packages.md) for more details.

## User Specified Packages

If a user [installs](../user_guide/install_packages.md) `pandas` via the command line, the specifications file will only list `pandas` and not all the specific dependencies of `pandas` for that specific architecture.

> This ensures that specifications file is platform independent whereas the [lock file](lockfile.md) is platform specific.

<div class="termy">

```console
$ ezconda install -n mlproj pandas

// Adds (only) pandas to mlproj.yml specifications file
```

</div>

??? Example "mlproj.yml"
    ```YAML
    # name of the environment
    name: mlproj

    # channels to search
    channels:
        - defaults
    
    # packages to install
    packages:
        - pandas
    ```
