# Release Notes


## :sparkles: **v0.8.0**

### :rocket: Features

* Add `update` command  (#36) @SarthakJariwala

<div class="termy">

```console
$ ezconda update -n sciml

// Update `sciml` environment according to `sciml.yml`
```
</div>

* Add summary option to `remove` command (#41) @SarthakJariwala

### :fire: Removals and Deprecations

* Remove `recreate` command (#37) @SarthakJariwala
> `recreate` was deprecated in v0.7.0.

### :hammer: Refactoring

* Refactor `subprocess.run` calls (#38) @SarthakJariwala

### :rotating_light: Testing

* Improve test coverage for `remove` command (#41) @SarthakJariwala


## :sparkles: **v0.7.0**

Requires Python>=3.7

### :rocket: Features

- `create` command can be used to create environments from lock file.

This unifies `create` command as the way to create new environments from scratch, from specifications file or from lock file.

<div class="termy">

```console
$ ezconda create --file mlproj-darwin-x86_64.lock

// Creates environment from mlproj-darwin-x86_64.lock
```
</div>

- Sync local conda environment with updated specifications file using `sync` command.

<div class="termy">

```console
$ ezconda sync -n ml-proj --with specfile

// Syncs 'ml-proj' environment with 'ml-proj.yml' file
```

</div>

- Sync local conda environment with updated lock file using `sync` command.

<div class="termy">

```console
$ ezconda sync -n ml-proj --with lockfile

// Syncs 'ml-proj' environment with corresponding lock file
```

</div>

### :fire: Deprecations

- `recreate` command is deprecated and will be removed in v0.8.0. Use `create` instead for creating new environments from lock file.

### :beetle: Fix

- `version` command now shows the correct version.

### :package: Build System

- `importlib-metadata` is now a dependency.
- Minimum supported version of Python is 3.7.

---

## :sparkles: **v0.6.0**

### :rocket: Features

- Add `summary` command to show environment summaries.

<div class="termy">

```console
$ ezconda summary --name sciml

// Shows environment summary for `sciml`
```
</div>

- Add `--summary` option to `create`, `install` and `remove` commands. By default, the option is set to `True` and will show environment summaries when commands are called.

### :construction_worker: CI System

- Changed `conda` GitHub action from `s-weigand/setup-conda@v1` to `conda-incubator/setup-miniconda@v2`.

---

## :sparkles: **v0.5.0**

### :rocket: Features

- Create a new environment from existing environment specifications ".yml" file.

<div class="termy">

```console
$ ezconda create --file sciml.yml

// Creates a new environment named `sciml` using `sciml.yml`
```
</div>

---

## :sparkles: **v0.4.0**

### :rocket: Features

- Lock file now checks for architecture and system specifications before attempting installation via `recreate` command.

    - If the specifications of the system do not match the lock file specifications, the `recreate` does not go forward. `create` should be used in that case.

    !!! Note
        This is different from how `conda` does explicit installtions. See docs for more information.
    
- Lock files also have a new `toml` based file format and new fields containing system specifications and other metadata.

> To upgrade to the new lock file format from a previous file format -

<div class="termy">

```console
$ ezconda lock --name ENVIRONMENT_NAME

// Generates new lock file for ENVIRONMENT_NAME
```
</div>

- New `config` command to set default solver

<div class="termy">

```console
$ ezconda config --solver mamba

// Default solver is set to mamba
```
</div>

- View current configurations


<div class="termy">

```console
$ ezconda config --show

// Prints current configurations
```
</div>


### :book: Documentation

- Add documentation on [design decisions](design_decisions/intro.md). Specifically, on specifications file and lock file.

- Update documentation related to lock file and config command.


### :construction_worker: CI System

- Add `release-drafter` workflow to GitHub Actions to update release notes as PRs are merged.

- Add `release` workflow to github actions to build and deploy using GitHub Actions.

---

## :sparkles: **v0.3.1**

### :beetle: Fix

- `ezconda version` now shows the correct version string.

<div class="termy">

```console
$ ezconda version
0.3.1
```

</div>

---

## :sparkles: **v0.3.0**

### :rocket: Features

- New option to select between `conda` and `mamba` solvers using `--solver` option.

<div class="termy">

```console
$ ezconda install -n env numpy --solver mamba
// Resolves environment using mamba
```

</div>

- Default solver is now set to `mamba`

### :book: Documentation

- Update installation instructions

---

## :sparkles: **v0.2.0**

Minor release with a new command - `lock`

### :rocket: Features

- New [`lock`](user_guide/lock_existing_env.md) command to generate a lock file for existing conda environments. See [docs](user_guide/lock_existing_env.md) for more information.

---

## :sparkles: **v0.1.0**

This is the first public release of `ezconda`.

Create, manage and re-create environments with an intuitive CLI.

### :rocket: Features

- Automatically create an environment specifications file as you create new environments.
- Auto update the specifications file as you install/remove packages from the environment.
- Create reproducible environments using an environment lock file (auto-generated/updated).
- Implements the following commands:
    - [`create`](user_guide/create_new_env.md)
    - [`install`](user_guide/install_packages.md)
    - [`remove`](user_guide/remove_packages.md)
    - [`recreate`]()
- [Autocompletions](user_guide/autocomplete.md) in your shell.

### :book: Documentation

- [Docs](https://ezconda.sarthakjariwala.com/) detailing features and user guide.