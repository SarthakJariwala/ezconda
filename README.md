# EZconda

![EZconda](https://github.com/SarthakJariwala/ezconda/blob/2945291bc9ef123cb52e9c6436906ac0728b0451/docs/logo.png)

<p align="center">
    <a href="https://github.com/SarthakJariwala/ezconda/actions?workflow=Tests">
        <img src="https://github.com/SarthakJariwala/ezconda/workflows/Tests/badge.svg">
    </a>
    <a href="https://codecov.io/gh/SarthakJariwala/ezconda">
        <img src="https://codecov.io/gh/SarthakJariwala/ezconda/branch/main/graph/badge.svg">
    </a>
    <a href="https://anaconda.org/conda-forge/ezconda">
        <img alt="Conda (channel only)" src="https://img.shields.io/conda/vn/conda-forge/ezconda">
    </a>
    <a href="https://ezconda.sarthakjariwala.com">
        <img src="https://github.com/SarthakJariwala/ezconda/workflows/Docs/badge.svg">
    </a>
</p>

<p align="center">
    <em><b>Create, Manage, Re-create</b> conda environments & specifications with ease.</em>
</p>

---

**EZconda** is a command line interface application that helps practitioners create and manage `conda` environment and related specifications with ease.

## Key Features

- **Environment specifications** : Add & remove packages from the <abbr title="commonly known as environment.yml file">specifications file</abbr> as you install & remove packages. _**No manual file edits!**_

- **Environment management** : Create & manage `conda` environments with ease.

- **Reproducible environments** : Lock current environment state and re-create it when necessary.

- **Easy to use & intuitive** : It very closely mimics `conda` API, so there is no new API to learn for users. Autocomplete for all shells.

- **Fast & Reliable Environment resolution** : Get fast and reliable environment solves by default. *EZconda* uses `mamba` by default, but you can easily switch between `mamba` and `conda`.

- **Best practices built-in** : Enforces the user to follow best `conda` practices.

## Requirements

- [Conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html) installation

## Installation

The recommended way to install **EZconda** is using `conda` or `mamba` in the `base` environment : 

### Using `conda`: 

```console
$ conda install ezconda -c conda-forge -n base
```

### Using `mamba`:

```console
$ mamba install ezconda -c conda-forge -n base
```

## Contributing Guidelines

<!-- TODO Add contributing guidelines -->

### Run tests

```bash
docker-compose up --build test
```

### Local iterative development

```bash
docker-compose build dev && docker-compose run dev bash
```