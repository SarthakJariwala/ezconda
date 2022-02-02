# Configurations

You can easily customize necessary **EZconda** behaviour using the `config` command.

## Set default solver

You can select between `conda` and `mamba` solvers for creating, resolving and installing packages. 

By default, **EZconda** uses `mamba` as the solver but you can change it easily using the `--solver` option with `config` command:

<div class="termy">

```console
$ ezconda config --solver conda

// Sets "conda" as the default solver
```

</div>

!!! Tip
    You can also override the default solver configuration whenever you need to by passing the `--solver` option.
    
    See [changing solvers](changing_solvers.md) for more information.


## View configurations

You can also view your current configurations using the `--show` option with the `config` command.

<div class="termy">

```console
$ ezconda config --show

// Shows current configurations

Current configuration

{
    "solver" : "conda"
}
```

</div>
