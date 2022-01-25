# Using a different solver

You can choose between `conda` and `mamba` for solving the environment by simply passing it to the `--solver` option.

**EZconda** uses `mamba` by default.

To use `mamba`:

<div class="termy">

```console
$ ezconda install  --solver mamba -n ds-proj numpy

// Uses mamba to resolve and install packages
```

</div>

!!! Info
    If you haven't heard of `mamba`, it offers higher speed and more reliable environment solutions. Learn more about `mamba` on their [website](https://mamba.readthedocs.io/en/latest/).

To use `conda`:

<div class="termy">

```console
$ ezconda install  --solver conda -n ds-proj numpy

// Uses conda to resolve and install packages
```

</div>

