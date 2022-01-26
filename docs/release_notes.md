# Release Notes


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
    - [`recreate`](user_guide/recreate_env.md)
- [Autocompletions](user_guide/autocomplete.md) in your shell.

### :book: Documentation

- [Docs](https://ezconda.sarthakjariwala.com/) detailing features and user guide.