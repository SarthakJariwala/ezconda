# Lock File

A lock file contains _**packages**_ that the user requested _**as well as all of it dependencies**_.

It contains the exact specifications of all the packages and their dependencies, version, build number, and channels.

Lock files are _**specific to the platform and architecture**_ they were generated on. 

!!! Note
    Information about the system's platform and architecture is also captured in the lock file and is used to validate the lock file when using it to recreate environments.

## Format

Lock file uses the following format to store the information described above -

```TOML
# minimum version of EZconda required
[version]
ezconda-min-version = "0.4.0"

# system specifications
[system]
platform = "darwin"
architecture = "64bit"
machine = "x86_64"

# name of the environment
[environment]
name = "mlproj"

# all the packages
[[packages]]
base_url = "https://conda.anaconda.org/conda-forge"
build_number = "0"
build_string = "py38h5fc983b_0"
channel = "conda-forge"
dist_name = "pandas-1.0.5-py38h5fc983b_0"
name = "pandas"
platform = "osx-64"
version = "1.0.5"

...
```

!!! Warning
    Lock files **are not meant to be edited by the user**. They are managed completely by EZconda. 

## Naming Convention

Lock files are named after the environment and the platform and its architecture.

```
<env>-<platform>-<architecture>.lock
```

For instance, if the environment name is "mlproj" and is created on a Mac, the name of the lock file will be -

```
mlproj-darwin-x86_64.lock
```

!!! Note
    This automatically ensures that same environment created on a different platform will have a separate lock file.