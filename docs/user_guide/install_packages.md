# Install Packages

**EZconda** will keep track of the packages you install in your environment and update the environment specifications file and lock file accordingly.

## Install packages

<div class="termy">

```console
$ ezconda install -n new-proj numpy pandas

// Installs numpy, pandas
🚀 Installed packages in new-proj

// Updates environment specifications
💾 Updated specifications to 'new-proj.yml'

// Updates lock file with new packages
🔒 Lock file updated
⭐ Done!
```
</div>

!!! Note
    The `-n` or `--name` flag is required while installing packages. This is a design decision to encourage best practices.
    
    If not provided, `ezconda` will prompt you to enter the environment name to install the package.

The new packages will be reflected in environment specification file - `new-proj.yml`.

```YAML hl_lines="5 6" title="new-proj.yml"
name: new-proj
channels:
    - defaults
dependencies:
    - numpy
    - pandas
```

!!! Note
    The specifications file only contains the packages listed on the command line and not their dependencies. 

The environment specifications file only contains the *specifications provided by the user*. A complete environment description is contained in the lock file.

For instance, `numpy` depends on `libopenblas` but `libopenblas` is not listed in the `dependencies` section of `new-proj.yml` above. 

However, the lock file contains `libopenblas` and all other dependencies of `numpy` as well as `pandas`.

Check it:

```TOML title="new-proj lock file"
[[packages]]
...
dist_name = "libopenblas-0.3.13-hf4835c0_1"
name = "libopenblas"

[[packages]]
...
dist_name = "numpy-1.21.2-py39h6fc94f6_0"
name = "numpy"

[[packages]]
...
dist_name = "numpy-base-1.21.2-py39h6ba5a95_0"
name = "numpy-base"
...
```

!!! Tip
    You can learn more about these differences and lock file [here](../design_decisions/lockfile.md).

## From specific channel

To install packages from a specific channel, pass the `-c` or `--channel` flag with the channel name.

<div class="termy">

```console
$ ezconda install -n new-proj -c conda-forge numpy pandas

// Installs numpy, pandas from conda-forge channel
```
</div>

```YAML hl_lines="3 6 7" title="new-proj.yml"
name: new-proj
channels:
    - conda-forge
    - defaults
dependencies:
    - numpy
    - pandas
```