# Environment Summary

You can get a summary of the changes made to the environment using the `summary` command.

## Latest transaction summary

You can specify the environment you want to get summary of using the `-n` or `--name` option:

<div class="termy">

```console
$ ezconda summary -n ml-proj

// Prints the latest transaction summary of ml-proj environment
```

</div>

!!! Note
    By default, the `summary` command shows the information about the latest transaction.

## For a specific revision

You can also specify the environment revision number for which you want the summary using `--revision`:

<div class="termy">

```console
$ ezconda summary -n ml-proj --revision 2

// Prints the summary of the 2nd environment transaction
```

</div>

## Summary for every command

You can get a summary of transactions with every command using the `--summary` option.

<div class="termy">

```console
$ ezconda install -n sciml numpy --summary

// Prints the summary of the transaction after command completes successfully
```

</div>

!!! Note

    The `--summary` option is passed to explicitly demonstrate its usage; `--summary` is passed by default for all commands.
    
    You can turn it off by passing `--no-summary`.
