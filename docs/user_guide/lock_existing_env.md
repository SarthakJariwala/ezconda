# Lock File for *Any* Environment

Having a lock file is required for *re-creating* environments. To facilitate this **EZconda** will generate and update environment lock file by default.

However, if you have an existing `conda` environment, you can use the `lock` command to generate a lock file for it.

## Lock *Any* Environment

Let's say you have an existing `conda` environment named `chem-ml`.

You can generate a lock file by providing `--name`/`-n`: 

<div class="termy">

```console
$ ezconda lock -n chem-ml

// Generates 'chem-ml.lock' file from existing `chem-ml` conda environment
```
</div>

!!! Note
    Lock files are platform specific as different platforms have different dependencies for certain packages. For information, see [discussion here](recreate_env.md#platform-specific-lock-files).

## Recreate Environment

Now, you can use `recreate` command to re-create the environment.

<div class="termy">

```console
$ ezconda recreate -n new-env chem-ml.lock

// Creates new environment 'new-env' from 'chem-ml.lock' file
```
</div>

!!! Info
    See [recreate](recreate_env.md) command for more information on reproducible environments.

