# Reproducible Environments

**EZconda** facilitates the creation of reproducible conda environments using a _**lock file**_ that it creates and maintains.

This is in addition to the *environment specifications* file (`environment.yml` file) that it already maintains for you.

Basically, anytime you perform an action on the conda environment using **EZconda**, it updates the specifications file as well as the _**lock file**_.

!!! Note
    The lock file is named after the environment name and the platform for which the environment was solved.

## `recreate`

To reproduce an environment, use the `recreate` command - 

<div class="termy">

```console
$ ezconda recreate new-proj-osx-64.lock

// Creates a new environment - 'new-proj-osx-64'

// Installs all the packages listed in the file
```
</div>

## Name the environment

You can provide a name for the new environment using the `-n` or `--name` option -

<div class="termy">

```console
$ ezconda recreate -n iris-2022 new-proj-osx-64.lock

// Creates a new environment - 'iris-2022' from the lock file
```
</div>

## Platform Specific Lock Files

Lock files are specific to the platform on which the environment was created. 

This means an environment specifications file `env.yml` on Mac and Linux will have two different lock files - `env-osx-64.lock` and `env-linux-aarch64.lock`. This is because packages might have different dependencies for different platforms.

For instance, installing `numpy` and `python=3.9` on *mac-osx-64* and *linux-aarch64* will result in slightly different dependencies.

=== "mac-osx-64"
    
    ```JSON hl_lines="4"
    numpy[1.22.0]
    ├─ libblas[3.9.0]
    ├─ libcblas[3.9.0]
    ├─ libcxx[12.0.1]
    ├─ liblapack[3.9.0]
    ├─ python[3.9.9]
    └─ python_abi[3.9]
    ```

=== "linux-aarch64"
    
    ```JSON hl_lines="4 5"
    numpy[1.22.0]
    ├─ libblas[3.9.0]
    ├─ libcblas[3.9.0]
    ├─ libgcc-ng[11.2.0]
    ├─ libstdcxx-ng[11.2.0]
    ├─ liblapack[3.9.0]
    ├─ python[3.9.9]
    └─ python_abi[3.9]
    ```
