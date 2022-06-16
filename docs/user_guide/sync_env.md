# Sync Local Environment

Use the **`sync`** command to sync local environment with any changes made to the environment specifications file (`.yml` file) or lock file (`.lock` file).

## Example

### Change made to specifications file

``` mermaid
sequenceDiagram
    actor Alice (Mac)
    participant Repository
    actor Bob (Windows)
    Note right of Alice (Mac): Create env, spec & lock file using EZconda
    Alice (Mac)->>Repository: Push env, spec & lock file
    Repository->>Bob (Windows): Pull changes
    Note right of Repository: Add new dependency to project
    Note right of Repository: Spec file changed
    Bob (Windows)->>Repository: Push changes made to spec file
    Repository->>Alice (Mac): Pull updated spec file
    Note right of Alice (Mac): Local environment <-Out of Sync-> New spec file
    Note right of Alice (Mac): Use `ezconda sync` to sync
```

!!! Tip
    **`sync`** command is useful when **any change** to the specifications file is **made manually or by a collaborator**.

### Change made to lock file

``` mermaid
sequenceDiagram
    actor Alice (Mac)
    participant Repository
    actor Bob (Mac)
    Note right of Alice (Mac): Create env, spec & lock file using EZconda
    Alice (Mac)->>Repository: Push env, spec & lock file
    Repository->>Bob (Mac): Pull changes
    Note right of Repository: Add new dependency to project
    Note right of Repository: Spec file & Lock file updated to reflect the new addition
    Bob (Mac)->>Repository: Push changes
    Repository->>Alice (Mac): Pull updated lock file
    Note right of Alice (Mac): Local environment <-Out of Sync-> New lock file
    Note right of Alice (Mac): Use `ezconda sync` to sync
```

## Sync an environment

Let's say the environment you want to sync is named `ml-proj`.

To sync it with the specifications file, use `sync` command with `--name`/`-n` option for environment name and `--with` option to explicitly specify `specfile` or `lockfile`:

### To sync with specifications file

<div class="termy">

```console
$ ezconda sync -n ml-proj --with specfile

// Syncs 'ml-proj' environment with 'ml-proj.yml' file
```

</div>

!!! Note
    If not specified, the environment specifications file is assumed to have the same filename as the environment name.

    `ml-proj` environment <--> `ml-proj.yml` specifications file

### To sync with lock file

<div class="termy">

```console
$ ezconda sync -n ml-proj --with lockfile

// Syncs 'ml-proj' environment with corresponding lock file
```

</div>


## Explicitly specify filename

If your specifications file name is not the same as the environment name, you can pass the file name using `--file` or `-f` option.

<div class="termy">

```console
$ ezconda sync -n ml-proj --file env.yml --with specfile

// Syncs 'ml-proj' environment with 'env.yml' file
```

</div>


## Using different solver

You can change the solver using `--solver` flag. 

By default, if not set using [`config`](configuration.md#set-default-solver), `mamba` will be used.

<div class="termy">

```console
$ ezconda sync -n ml-proj --with specfile --solver conda

// Syncs 'ml-proj' environment with 'ml-proj.yml' file using 'conda' solver
```

</div>