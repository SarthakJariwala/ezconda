# From specifications file

If you have a specifications file (`.yml` file) that you want to use for creating an environment, you can use the `--file` option with `create` command.

Environment specifications file:

```yaml title="sciml.yml"
name: sciml
channels:
    - defaults
    - conda-forge
dependencies:
    - python=3.9
    - numpy
    - pandas
```

<div class="termy">

```console
$ ezconda create --file sciml.yml

// Creates a new environment named `sciml` using `sciml.yml`
```
</div>