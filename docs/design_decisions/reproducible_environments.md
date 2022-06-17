# Reproducible Environments

**EZconda** facilitates the creation of reproducible conda environments using a _**lock file**_ that it creates and maintains.

This is in addition to the *environment specifications* file (`environment.yml` file) that it already maintains for you.

Basically, anytime you perform an action on the conda environment using **EZconda**, it updates the specifications file as well as the _**lock file**_.

!!! Note
    The lock file is named after the environment name and the platform and architecture for which the environment was solved.


## Platform Specific Lock Files

Lock files are specific to the platform on which the environment was created. 

This means an environment specifications file `env.yml` on Mac and Linux will have two different lock files - `env-darwin-x86_64.lock` and `env-linux-aarch64.lock`. This is because packages might have different dependencies for different platforms.

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

## Lock file validation

If a lock file generated on a Mac is used to recreate an environment on a Linux machine, **EZconda** will throw a lock file validation error instead of creating broken environments.

!!! Note
    This is different from how `conda` recreates environments from *explicit* specifications file. 
