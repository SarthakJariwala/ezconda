# Remove Packages

**EZconda** will keep track of the packages you remove from your environment and update the environment specifications file and lock file accordingly.

If a package that you are trying to remove is a dependency for another installed package, **EZconda** will inform you about this before continuing. (More on this [later](#dependencies))

## Remove packages

Let's say you have installed `numpy` and `python=3.9` in your environment `new-proj` and the specifications file looks like this -

```YAML title="new-proj.yml"
name: new-proj
channels:
    - defaults
dependencies:
    - python=3.9
    - numpy
```

To remove `numpy` from the environment, use the `remove` command -

<div class="termy">

```console
$ ezconda remove -n new-proj numpy

// Removes numpy from new-proj
🚀 Removed packages from new-proj
 
// Updates environment specifications
💾 Updated specifications to 'new-proj.yml'

// Updates lock file with new packages
🔒 Lock file updated
⭐ Done!
```
</div>

The updated specifications file and lock file does not contain `numpy` - 

```YAML title="new-proj.yml"
name: new-proj
channels:
    - defaults
dependencies:
    - python=3.9
```

## Dependencies

**EZconda** performs informed package removal.

Let's say you have installed both `numpy` and `pandas` in your environment and the specification file looks like the following - 

```YAML title="new-proj.yml" hl_lines="6 7"
name: new-proj
channels:
    - defaults
dependencies:
    - python=3.9
    - numpy
    - pandas
```

Now, if you try to remove `numpy` from the environment, **EZconda** will inform you that `pandas` requires `numpy` to be installed and if you remove it, `pandas` will also be removed from the environment.

Check it out - 

<div class="termy">

```console
$ ezconda remove -n new-proj numpy

// Identifies dependent packages
There are packages that depend on 'numpy'

Removing 'numpy' will also remove them!

numpy is required by
- pandas

// Asks before continuing
Do you want to continue? [y/N]: 
```
</div>