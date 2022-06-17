# Lock File for *Any* Environment

Having a [lock file](../design_decisions/lockfile.md) is required for *re-creating* exact environments. **EZconda** will generate and update environment lock file by default.

However, if you have an existing `conda` environment, you can use the `lock` command to generate a lock file for it.

## Lock *Any* Environment

Let's say you have an existing `conda` environment named `chem-ml`.

You can generate a lock file by providing `--name`/`-n`: 

<div class="termy">

```console
$ ezconda lock -n chem-ml

// Generates a lock file from existing `chem-ml` conda environment
```
</div>

!!! Info
    Lock files are platform specific as different platforms have different dependencies for certain packages. For information, see [discussion here](../design_decisions/reproducible_environments.md#platform-specific-lock-files).

## Recreate Environment

Now, you can use `create` command to re-create the environment using lock file. See [create](./create_new_env_from_lockfile.md) command for more information on creating environments.


<div class="termy">

```console
$ ezconda create -n new-env --file chem-ml.lock

// Creates new environment 'new-env' from 'chem-ml.lock' file
```
</div>

!!! Note
    Creating environments from lock file only work for the system/platform for which the lock file was generated.
    
    To understand why, check out [platform specific lock files](../design_decisions/reproducible_environments.md#platform-specific-lock-files).

