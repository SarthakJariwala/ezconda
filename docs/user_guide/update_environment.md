# Update Complete Environment

To update an existing `conda` environment (created using **EZconda**), you can use the `update` command.

## Update environment

<div class="termy">

```console
$ ezconda update -n sciml

// Update `sciml` environment according to `sciml.yml`
```
</div>


## Specify environment file

<div class="termy">

```console
$ ezconda update -n sciml --file env.yml

// Update `sciml` environment according to `env.yml`
```
</div>

!!! Note
    If no environment specifications file is passed using `--file` option, EZconda will search and use the specifications file named after the environment.
